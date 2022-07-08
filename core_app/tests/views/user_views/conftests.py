import pytest
from innotter_page.serializers import PageSerializer
from innotter_user.models import User
from innotter_user.serializers import UsernameSerializer
from model_bakery import baker
from rest_framework.test import APIRequestFactory, force_authenticate


@pytest.fixture()
def user():
    user = baker.make(User)
    user.role = "admin"
    user.save()
    return user


@pytest.fixture()
def new_user():
    return baker.prepare(User)


@pytest.fixture()
def update_json(new_user: User):
    return {
        "user": {
            "email": new_user.email,
            "username": new_user.username,
        }
    }


@pytest.fixture()
def expected_json(user: User):
    return {
        "email": user.email,
        "username": user.username,
        "is_active": user.is_active,
        "is_staff": user.is_staff,
        "role": user.role,
        "title": user.title,
        "pages": PageSerializer(user.pages.all(), many=True).data,
        "refresh_token": user.refresh_token,
        "follows": UsernameSerializer(user.follows.all(), many=True).data,
        "is_blocked": user.is_blocked,
    }


@pytest.fixture()
def expected_update_json(user: User, new_user: User):
    return {
        "email": new_user.email,
        "username": new_user.username,
        "title": user.title,
        "is_staff": user.is_staff,
        "is_active": user.is_active,
        "role": user.role,
        "pages": PageSerializer(user.pages.all(), many=True).data,
        "refresh_token": new_user.refresh_token,
        "follows": UsernameSerializer(user.follows.all(), many=True).data,
        "is_blocked": new_user.is_blocked,
    }


@pytest.fixture()
def api_factory():
    return APIRequestFactory()
