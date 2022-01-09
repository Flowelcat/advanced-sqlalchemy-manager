import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from alchmanager.alchmanager import ManagedQuery, BaseQueryManager
from alchmanager.alchmanager import ManagedSession
from tests.models import Book, Person, Student, Base, Exam


class BookQueryManager(BaseQueryManager):
    __model__ = Book

    @staticmethod
    def has_in_title(query, title_part):
        return query.filter(Book.title.contains(title_part))


class PersonQueryManager(BaseQueryManager):
    __model__ = Person

    @staticmethod
    def older_than(query, age):
        return query.filter(Person.age > age)

    @staticmethod
    def younger_than(query, age):
        return query.filter(Person.age < age)

    @staticmethod
    def first_of_exact_age(query, age):
        return query.filter(Person.age == age).first()


@pytest.fixture(autouse=True)
def create_db(request):
    engine = create_engine('sqlite:///:memory:')
    session_factory = sessionmaker(query_cls=ManagedQuery, class_=ManagedSession, bind=engine)
    session = session_factory()

    Base.metadata.create_all(engine)

    session.add(Person(name="Person 1", age=25))
    session.add(Person(name="Person 2", age=60))
    student_1 = Student(name="Student 1", age=21, subject="Mathematics")
    student_2 = Student(name="Student 2", age=23, subject="Physics")
    session.add(student_1)
    session.add(student_2)
    session.add(Exam(title="Mathematics", score=94, student=student_1))
    session.add(Exam(title="Physics", score=75, student=student_2))

    session.add(Book(title="Best book ever", is_public=True))
    session.add(Book(title="Small specific book", is_public=False))

    session.commit()
    request.cls.session = session

    @session.load_manager()
    class SessionManager(BaseQueryManager):
        @staticmethod
        def is_book_public(query):
            return query.filter(Book.is_public.is_(True))
