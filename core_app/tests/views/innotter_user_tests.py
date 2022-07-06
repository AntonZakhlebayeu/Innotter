from unittest import mock

import pytest
from innotter_page.serializers import PageSerializer
from innotter_user.models import User
from innotter_user.serializers import UsernameSerializer
from innotter_user.views import UserViewSet
from model_bakery import baker
from rest_framework.test import APIRequestFactory, force_authenticate

api_factory = APIRequestFactory()
register_view = UserViewSet.as_view({"post": "register"})
login_view = UserViewSet.as_view({"post": "login"})
users_view = UserViewSet.as_view(
    {"get": "retrieve", "put": "update", "delete": "destroy"}
)

pytestmark = pytest.mark.django_db


class TestUserEndpoints:
    endpoint = "/api/users/"

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_register(
        self,
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
            self.endpoint,
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
    @mock.patch(
        "innotter_user.serializers.LoginSerializer.is_valid", return_value=True
    )
    def test_login(self, mock_is_valid):
        user = baker.make(User)

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

        with mock.patch(
            "innotter_user.serializers.LoginSerializer.data", user_json
        ):
            request = api_factory.post(
                f"{self.endpoint}/login/",
                login_json,
                format="json",
            )

            response = login_view(request)
            assert response.status_code == 200
            assert response.data == user_json

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_retrieve(self):
        user = baker.make(User)
        user.role = "admin"
        user.save()

        expected_json = {
            "email": user.email,
            "username": user.username,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "role": user.role,
            "pages": PageSerializer(user.pages.all(), many=True).data,
            "refresh_token": user.refresh_token,
            "follows": UsernameSerializer(user.follows.all(), many=True).data,
            "is_blocked": user.is_blocked,
        }

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
    def test_delete(self):
        user = baker.make(User)
        user.role = "admin"

        request = api_factory.delete(f"{self.endpoint}/{user.pk}/")

        force_authenticate(request, user=user, token=user.access_token)
        response = users_view(request, pk=user.pk)

        assert response.status_code == 204
        assert User.objects.all().count() == 0
