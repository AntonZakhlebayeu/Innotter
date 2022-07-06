from unittest import mock

import pytest
from innotter_user.views import RegistrationAPIView
from rest_framework.test import APIRequestFactory

api_factory = APIRequestFactory()
view = RegistrationAPIView.as_view()


class TestUserEndpoints:

    endpoint = "/api/users/"

    @pytest.mark.django_db
    @mock.patch("innotter_user.serializers.RegistrationSerializer.save")
    def test_register(self, mock_save):
        mock_save.return_value = True

        user_json = {
            "user": {
                "email": "user7@user.user",
                "username": "user7",
                "password": "qweasdzxc",
            }
        }

        request = api_factory.post(
            self.endpoint,
            user_json,
            format="json",
        )

        response = view(request)

        assert response.status_code == 201
