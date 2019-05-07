import re
import os
import pytest
import sqlalchemy
from sqlalchemy import create_engine
import factory

from api import app as flask_app
from api.lib.database import db


@pytest.fixture(scope='session')
def database(request):
    """Create a fresh database for the tests"""
    db_uri = os.getenv('SQLALCHEMY_DATABASE_URI')

    # connect to template1 to create test database
    template_db_uri = re.sub(r'\/\w+$', '/template1', db_uri)
    engine = create_engine(template_db_uri)
    connection = engine.connect()

    db_conn_parts = sqlalchemy.engine.url.make_url(db_uri).translate_connect_args()
    connection.execute('commit')
    connection.execute('drop database if exists %s' % db_conn_parts['database'])
    connection.execute('commit')
    connection.execute('create database %s' % db_conn_parts['database'])
    connection.close()

    yield db_uri


@pytest.fixture(scope='session')
def app(database):
    """Create a Flask app context for the tests"""
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = database

    with flask_app.app_context():
        yield flask_app


@pytest.fixture(scope='session')
def client(app):
    """Create instance of Flask test client"""
    return app.test_client()


@pytest.fixture(scope='session')
def _db(app):
    """Create database tables and return test database"""
    db.create_all()
    return db


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Base class for factories"""
    class Meta:
        sqlalchemy_session_persistence = 'commit'
