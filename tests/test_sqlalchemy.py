from tests.conftest import Person, Book, Student
from tests.models import Exam


class TestsQueryManager:

    def test_simple_query(self):
        standard_query = self.session.query(Person).filter(Person.age > 30).all()
        managed_query = self.session.query(Person).older_than(30).all()
        assert standard_query == managed_query

    def test_chained_query(self):
        standard_query = self.session.query(Person).filter(Person.age > 18).filter(Person.age < 40).all()
        managed_query = self.session.query(Person).older_than(18).younger_than(40).all()
        assert standard_query == managed_query

    def test_chained_with_filter_query(self):
        standard_query = self.session.query(Person).filter(Person.age > 18).filter(Person.name.contains("1")).filter(Person.age < 40).all()
        managed_query = self.session.query(Person).older_than(18).filter(Person.name.contains("1")).younger_than(40).all()
        assert standard_query == managed_query

    def test_complete_query(self):
        standard_query = self.session.query(Person).filter(Person.age == 25).first()
        managed_query = self.session.query(Person).first_of_exact_age(25)
        assert standard_query == managed_query

    def test_without_manager(self):
        assert not hasattr(self.session.query(Book), 'is_public')
        assert hasattr(self.session.query(Book).filter(Book.is_public.is_(True)).first(), 'is_public')

    def test_with_attribute(self):
        standard_query = self.session.query(Person.age).filter(Person.age > 50).filter(Person.age < 100)
        managed_query = self.session.query(Person.age).older_than(50).younger_than(100)
        assert str(standard_query) == str(managed_query)
        assert managed_query.scalar() == 60

    def test_with_multiple_attributes(self):
        standard_query = self.session.query(Person.name, Person.age).filter(Person.age > 50).filter(Person.age < 100)
        managed_query = self.session.query(Person.name, Person.age).older_than(50).younger_than(100)
        assert str(standard_query) == str(managed_query)
        assert managed_query.first() == ("Person 2", 60)

    def test_with_multiple_models(self):
        standard_query = self.session.query(Exam, Person).join(Exam.student).filter(Person.age > 20).filter(Person.age < 40).filter(Exam.score > 80)
        managed_query = self.session.query(Exam, Person).join(Exam.student).older_than(20).younger_than(40).filter(Exam.score > 80)
        assert str(standard_query) == str(managed_query)
        exam, student = managed_query.first()
        assert exam.score == 94
        assert student.name == "Student 1"


class TestsSessionManager:

    def test_is_loaded(self):
        assert hasattr(self.session.query(Book), 'is_book_public')

    def test_is_loaded_on_any_model(self):
        assert hasattr(self.session.query(Student), 'is_book_public')
        self.session.query(Student).is_book_public().all()

    def test_simple_query(self):
        assert self.session.query(Book).is_book_public().count() == 1
        assert self.session.query(Book).count() == 2

    def test_general_managed_query(self):
        assert hasattr(self.session.query(Book), 'has_in_title')
        assert self.session.query(Book).has_in_title('specific').first() is not None

    def test_chained(self):
        book_count = self.session.query(Book).is_book_public().has_in_title('book').count()
        assert book_count == 1
