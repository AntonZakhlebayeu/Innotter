import pytest
from apiclient import APIClient
from factories.user_factory import UserFactory
from pytest_factoryboy import register

register(UserFactory)
