import pytest
from factories.user_factory import UserFactory
from pytest_factoryboy import register

register(UserFactory)


@pytest.fixture
def new_user(db, user_factory):
    user = user_factory.create()
    return user
