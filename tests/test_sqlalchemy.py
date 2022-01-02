from tests.conftest import Person, Book, Student


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
