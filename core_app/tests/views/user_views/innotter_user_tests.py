from unittest import mock

import pytest
from innotter_user.models import User
from innotter_user.serializers import UserSerializer
from innotter_user.views import UserViewSet
from model_bakery import baker
from rest_framework.test import APIRequestFactory, force_authenticate
from tests.views.conftests import api_factory
from tests.views.user_views.conftests import (
    expected_json,
    expected_update_json,
    new_user,
    update_json,
    user,
)

register_view = UserViewSet.as_view({"post": "register"})
login_view = UserViewSet.as_view({"post": "login"})
users_view = UserViewSet.as_view(
    {"get": "retrieve", "put": "update", "delete": "destroy"}
)
list_view = UserViewSet.as_view({"get": "list"})
me_view = UserViewSet.as_view({"get": "me", "put": "update_me"})
block_view = UserViewSet.as_view({"put": "block"})
unblock_view = UserViewSet.as_view({"put": "unblock"})

pytestmark = pytest.mark.django_db


class TestUserEndpoints:
    endpoint = "/api/users/"

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_register(
        self,
        api_factory: APIRequestFactory,
    ):
        user_json = {
            "user": {
                "email": "user7@user.user",
                "username": "user7",
                "password": "qweasdzxc",
                "role": "user",
                "title": "test title",
            }
        }

        request = api_factory.post(
            f"{self.endpoint}register",
            user_json,
            format="json",
        )

        response = register_view(request)
        user_json["user"].pop("password")
        user = User.objects.first()
        user_json["user"]["access_token"] = user.access_token
        user_json["user"]["refresh_token"] = user.refresh_token

        assert response.data == user_json.get("user")
        assert response.status_code == 201

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    @mock.patch("innotter_user.serializers.LoginSerializer.is_valid", return_value=True)
    def test_login(self, mock_is_valid, user: user, api_factory: APIRequestFactory):
        login_json = {
            "user": {
                "email": user.email,
                "password": user.password,
            }
        }

        user_json = {
            "email": user.email,
            "username": user.username,
            "access_token": user.access_token,
            "refresh_token": user.refresh_token,
        }

        with mock.patch("innotter_user.serializers.LoginSerializer.data", user_json):
            request = api_factory.post(
                f"{self.endpoint}/login/",
                login_json,
                format="json",
            )

            response = login_view(request)
            assert response.status_code == 200
            assert response.data == user_json

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_list(self, user: user, api_factory: APIRequestFactory):
        baker.make(User, _refresh_after_create=True, _quantity=4)

        request = api_factory.get(self.endpoint)

        force_authenticate(request, user=user, token=user.access_token)
        response = list_view(request)

        assert response.status_code == 200
        assert len(response.data) == 5

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_retrieve(
        self,
        user: user,
        expected_json: expected_json,
        api_factory: APIRequestFactory,
    ):
        expected_json = expected_json

        request = api_factory.get(f"{self.endpoint}{user.pk}/")
        force_authenticate(request, user=user, token=user.access_token)
        request.COOKIES["access_token"] = user.access_token
        request.COOKIES["refresh_token"] = user.refresh_token

        response = users_view(request, pk=user.pk)
        expected_json["access_token"] = user.access_token

        assert response.status_code == 200
        assert response.data == expected_json
        assert response.cookies["access_token"].value == user.access_token

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_update(
        self,
        user: user,
        update_json: update_json,
        expected_update_json: expected_update_json,
        api_factory: APIRequestFactory,
    ):
        current_user = baker.make(User)
        current_user.role = "admin"
        current_user.save()

        user_json = update_json
        expected_json = expected_update_json

        old_user = User.objects.get(pk=user.pk, role=user.role)

        request = api_factory.put(
            f"{self.endpoint}{old_user.pk}/",
            user_json,
            format="json",
        )

        force_authenticate(request, user=current_user, token=current_user.access_token)
        response = users_view(request, pk=old_user.pk)

        assert response.status_code == 200
        assert response.data == expected_json

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_retrieve_me(self, user: user, api_factory: APIRequestFactory):
        request = api_factory.get(
            f"{self.endpoint}me/",
        )
        force_authenticate(request, user=user, token=user.access_token)
        response = me_view(request)

        assert response.status_code == 200
        assert response.data == UserSerializer(user).data

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_update_me(
        self,
        user: user,
        update_json: update_json,
        expected_update_json: expected_update_json,
        api_factory: APIRequestFactory,
    ):
        user_json = update_json
        expected_json = expected_update_json

        request = api_factory.put(
            f"{self.endpoint}update_me/",
            user_json,
            format="json",
        )

        force_authenticate(request, user=user, token=user.access_token)
        response = me_view(request)

        assert response.status_code == 200
        assert response.data == expected_json

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_delete(self, user: user, api_factory: APIRequestFactory):
        request = api_factory.delete(f"{self.endpoint}/{user.pk}/")

        force_authenticate(request, user=user, token=user.access_token)
        response = users_view(request, pk=user.pk)

        assert response.status_code == 204
        assert User.objects.all().count() == 0

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_block(self, user: user, new_user: new_user, api_factory: APIRequestFactory):
        user_to_block = new_user
        user_to_block.save()

        request = api_factory.put(f"{self.endpoint}/{user_to_block.pk}/block/")
        force_authenticate(request, user=user, token=user.access_token)
        response = block_view(request, pk=user_to_block.pk)

        assert response.status_code == 200
        assert User.objects.get(pk=user_to_block.pk).is_blocked is True

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_unblock(
        self, user: user, new_user: new_user, api_factory: APIRequestFactory
    ):
        user_to_unblock = new_user
        user_to_unblock.is_blocked = True
        user_to_unblock.save()

        request = api_factory.put(f"{self.endpoint}/{user_to_unblock.pk}/unblock/")
        force_authenticate(request, user=user, token=user.access_token)
        response = unblock_view(request, pk=user_to_unblock.pk)

        assert response.status_code == 200
        assert User.objects.get(pk=user_to_unblock.pk).is_blocked is False
