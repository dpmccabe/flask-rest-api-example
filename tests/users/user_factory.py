import pytest
import factory

from api.models.user import User

from tests.conftest import BaseFactory


@pytest.fixture
def UserFactory(db_session):
    """need to wrap factories in a fixture to use db_session fixture"""
    class _UserFactory(BaseFactory):
        class Meta:
            model = User
            sqlalchemy_session = db_session

        id = factory.Faker('uuid4')
        name = factory.Faker('name')
        email = factory.Faker('email')

    return _UserFactory
