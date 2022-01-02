# Managers for SQLAlchemy.
Manager for model, methods were added during runtime to query.

## Installation

```
    $ [sudo] pip install advanced-sqlalchemy-manager
```

## Documentation

### ManagedQuery
Managed query that replaces sqlalchemy.query class

### Example:

```python
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from alchmanager import ManagedQuery, BaseQueryManager

engine = create_engine('sqlite:///:memory:')
session_factory = sessionmaker(query_cls=ManagedQuery, bind=engine)
session = session_factory()

Base = declarative_base()


class Person(Base):
    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    age = Column(Integer, nullable=False)


class PersonQueryManager(BaseQueryManager):
    __model__ = Person

    @staticmethod
    def older_than(query: ManagedQuery, age: int) -> ManagedQuery:
        return query.filter(Person.age > age)

    @staticmethod
    def younger_than(query: ManagedQuery, age: int):
        return query.filter(Person.age < age)

    @staticmethod
    def first_of_exact_age(query: ManagedQuery, age: int):
        return query.filter(Person.age == age).first()


filtered_persons = session.query(Person).older_than(30).filter(Person.name.contains('_')).younger_than(60).all()
person_25_years_old = session.query(Person).first_of_exact_age(25)
```

### ManagedSession

Managed session. 
Use decorator ``load_manager()`` to register query managers into session.
Registered that way session managers will be usable on any model.

### Example:

```python
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from alchmanager import ManagedQuery, ManagedSession, BaseQueryManager

engine = create_engine('sqlite:///:memory:')
session_factory = sessionmaker(class_=ManagedSession, bind=engine)
session = session_factory()

Base = declarative_base()


class Person(Base):
    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    age = Column(Integer, nullable=False)


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String)

    is_public = Column(Boolean, nullable=False, default=False)


@session.load_manager()
class BookQueryManager(BaseQueryManager):
    @staticmethod
    def is_book_public(query: ManagedQuery) -> ManagedQuery:
        return query.filter(Book.is_public.is_(True))


count_of_filtered_books = session.query(Book).is_book_public().count()

# This will produce broken query because is_public does not exists in Person model
persons = session.query(Person).is_book_public().count()
```