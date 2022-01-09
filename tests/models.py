from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Person(Base):
    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    age = Column(Integer, nullable=False)

    type = Column(String, nullable=False, default="person")

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'person',
    }


class Student(Person):
    __tablename__ = 'students'

    subject = Column(String, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'student',
        'inherit_condition': (Person.type == 'student')
    }


class Exam(Base):
    __tablename__ = 'exams'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    score = Column(Float(), nullable=False)

    student_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    student = relationship("Person", backref="exam")


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String)

    is_public = Column(Boolean, nullable=False, default=False)
