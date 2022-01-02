import flask
import pytest
from flask_sqlalchemy import SQLAlchemy

from alchmanager.alchmanager import ManagedQuery
from tests.models import Base, Person, Book, Student

app = flask.Flask(__name__)
db = SQLAlchemy(query_class=ManagedQuery, model_class=Base)


@app.route('/run_simple_query', methods=['POST'])
def run_simple_query():
    standard_query = db.session.query(Person).filter(Person.age > 30).all()
    managed_query = db.session.query(Person).older_than(30).all()

    try:
        assert standard_query == managed_query
    except AssertionError:
        flask.abort(500)
    return ''


@app.route('/run_chained_query', methods=['POST'])
def run_chained_query():
    try:
        standard_query = db.session.query(Person).filter(Person.age > 18).filter(Person.age < 40).all()
        managed_query = db.session.query(Person).older_than(18).younger_than(40).all()
        assert standard_query == managed_query
    except AssertionError:
        flask.abort(500)

    return ''


@app.route('/run_chained_with_filter_query', methods=['POST'])
def run_chained_with_filter_query():
    try:
        standard_query = db.session.query(Person).filter(Person.age > 18).filter(Person.name.contains("1")).filter(Person.age < 40).all()
        managed_query = db.session.query(Person).older_than(18).filter(Person.name.contains("1")).younger_than(40).all()
        assert standard_query == managed_query
    except AssertionError:
        flask.abort(500)

    return ''


@app.route('/run_complete_query', methods=['POST'])
def run_complete_query():
    try:
        standard_query = db.session.query(Person).filter(Person.age == 25).first()
        managed_query = db.session.query(Person).first_of_exact_age(25)
        assert standard_query == managed_query
    except AssertionError:
        flask.abort(500)

    return ''


@app.route('/run_without_manager', methods=['POST'])
def run_without_manager():
    try:
        assert not hasattr(db.session.query(Book), 'is_public')
        assert hasattr(db.session.query(Book).filter(Book.is_public.is_(True)).first(), 'is_public')
    except AssertionError:
        flask.abort(500)

    return ''


@pytest.fixture()
def client():
    class Config:
        DEBUG = False
        TESTING = True

        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        SQLALCHEMY_TRACK_MODIFICATIONS = True

    app.config.from_object(Config())

    with app.test_client() as client:
        with app.app_context():
            db.init_app(app)
            db.create_all()

            db.session.add(Person(name="Person 1", age=25))
            db.session.add(Person(name="Person 2", age=60))
            db.session.add(Student(name="Student 1", age=21, subject="Mathematics"))
            db.session.add(Student(name="Student 2", age=23, subject="Physics"))
            db.session.add(Book(title="Best book ever", is_public=True))
            db.session.add(Book(title="Small specific book", is_public=False))
            db.session.commit()

    yield client


class TestsQueryManager:

    def test_simple_query(self, client):
        response = client.post('/run_simple_query')
        assert response.status_code == 200

    def test_chained_query(self, client):
        response = client.post('/run_chained_query')
        assert response.status_code == 200

    def test_chained_with_filter_query(self, client):
        response = client.post('/run_chained_with_filter_query')
        assert response.status_code == 200

    def test_complete_query(self, client):
        response = client.post('/run_complete_query')
        assert response.status_code == 200

    def test_without_manager(self, client):
        response = client.post('/run_without_manager')
        assert response.status_code == 200
