import json
from unittest import mock

import pytest
from innotter_user.models import User
from innotter_user.views import LoginAPIView, RegistrationAPIView
from model_bakery import baker
from rest_framework.test import APIRequestFactory

api_factory = APIRequestFactory()
register_view = RegistrationAPIView.as_view()
login_view = LoginAPIView.as_view()

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
        user_json["user"]["access_token"] = User.objects.first().access_token
        user_json["user"]["refresh_token"] = User.objects.first().refresh_token

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
