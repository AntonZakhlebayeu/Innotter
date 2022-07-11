from unittest import mock

import pytest
from innotter_page.models import Page
from innotter_page.serializers import PageSerializer
from innotter_page.views import PageList
from model_bakery import baker
from rest_framework.test import APIRequestFactory, force_authenticate
from tests.views.conftests import api_factory
from tests.views.page_views.conftests import (
    block_json,
    expected_json,
    expected_update_json,
    new_page,
    page,
    update_json,
)
from tests.views.user_views.conftests import user

pytestmark = pytest.mark.django_db

page_viewset = PageList.as_view(
    {
        "post": "create",
        "get": "retrieve",
        "put": "update",
        "delete": "destroy",
    }
)

block_viewset = PageList.as_view({"put": "block"})
unblock_viewset = PageList.as_view({"put": "unblock"})

list_page_viewset = PageList.as_view({"get": "list"})


class TestPageEndpoint:
    endpoint = "api/pages/"

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_create(
        self, user: user, new_page: new_page, api_factory: APIRequestFactory
    ):
        page_json = {
            "uuid": new_page.uuid,
            "name": new_page.name,
            "description": new_page.description,
            "is_private": new_page.is_private,
        }

        request = api_factory.post(self.endpoint, page_json, format="json")
        force_authenticate(request, user=user, token=user.access_token)

        response = page_viewset(request)

        assert response.status_code == 201
        assert (
            response.data
            == PageSerializer(Page.objects.get(uuid=new_page.uuid)).data
        )

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_retrieve(
        self,
        user: user,
        page: page,
        api_factory: APIRequestFactory,
        expected_json: expected_json,
    ):
        request = api_factory.get(f"{self.endpoint}{page.pk}/")
        force_authenticate(request, user=user, token=user.access_token)

        response = page_viewset(request, pk=page.pk)

        assert response.status_code == 200
        assert response.data == expected_json

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_list(self, user: user, api_factory: APIRequestFactory):
        baker.make(Page, _quantity=3)

        request = api_factory.get(self.endpoint)
        force_authenticate(request, user=user, token=user.access_token)

        response = list_page_viewset(request)

        assert response.status_code == 200
        assert len(response.data) == 3

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_update(
        self,
        user: user,
        page: page,
        update_json: update_json,
        expected_update_json: expected_update_json,
        api_factory: APIRequestFactory,
    ):
        request = api_factory.put(
            f"{self.endpoint}{page.pk}", update_json, format="json"
        )
        force_authenticate(request, user=user, token=user.access_token)

        response = page_viewset(request, pk=page.pk)

        assert response.status_code == 200
        assert response.data == expected_update_json

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_delete(
        self, user: user, page: page, api_factory: APIRequestFactory
    ):
        request = api_factory.delete(f"{self.endpoint}{page.pk}")
        force_authenticate(request, user=user, token=user.access_token)

        response = page_viewset(request, pk=page.pk)

        assert response.status_code == 204
        assert Page.objects.all().count() == 0

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_block(
        self,
        user: user,
        page: page,
        block_json: block_json,
        expected_json: expected_json,
        api_factory: APIRequestFactory,
    ):
        request = api_factory.put(
            f"{self.endpoint}{page.pk}/block/", block_json, format="json"
        )
        force_authenticate(request, user=user, token=user.access_token)

        response = block_viewset(request, pk=page.pk)

        assert response.status_code == 200
        assert not Page.objects.get(pk=page.pk).is_temporary_blocked()

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_unblock(
        self, user: user, page: page, api_factory: APIRequestFactory
    ):
        request = api_factory.put(
            f"{self.endpoint}{page.pk}/unblock/", {"page": {}}, format="json"
        )
        force_authenticate(request, user=user, token=user.access_token)

        response = unblock_viewset(request, pk=page.pk)

        assert response.status_code == 200
        assert Page.objects.get(pk=page.pk).is_temporary_blocked()
