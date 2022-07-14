from unittest import mock

import pytest
from innotter_tag.models import Tag
from innotter_tag.serializers import TagSerializer
from innotter_tag.views import TagList
from model_bakery import baker
from rest_framework.test import APIRequestFactory, force_authenticate
from tests.views.conftests import api_factory
from tests.views.page_views.conftests import page
from tests.views.tags_views.conftests import tag
from tests.views.user_views.conftests import user

pytestmark = pytest.mark.django_db

tag_viewset = TagList.as_view({"get": "retrieve", "post": "create", "delete": "destroy"})
list_viewset = TagList.as_view({"get": "list"})


class TestTagEndpoint:
    endpoint = "api/pages/"

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_create(self, user: user, page: page, api_factory: APIRequestFactory):
        request = api_factory.post(
            f"{self.endpoint}{page.pk}/tags", {"name": "test"}, format="json"
        )

        force_authenticate(request, user=user, token=user.access_token)

        response = tag_viewset(request, pages_pk=page.pk)

        assert response.status_code == 201
        assert page.tags.all().count() == 1
        assert page.tags.first() == Tag.objects.first()

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_retrieve(
        self, user: user, page: page, tag: tag, api_factory: APIRequestFactory
    ):
        request = api_factory.get(f"{self.endpoint}{page.pk}/tags/{tag.pk}/")
        force_authenticate(request, user=user, token=user.access_token)

        response = tag_viewset(request, pages_pk=page.pk, pk=tag.pk)

        assert response.status_code == 200
        assert TagSerializer(page.tags.first()).data == response.data

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_destroy(
        self, user: user, page: page, tag: tag, api_factory: APIRequestFactory
    ):
        request = api_factory.delete(f"{self.endpoint}{page.pk}/tags/{tag.pk}")
        force_authenticate(request, user=user, token=user.access_token)

        response = tag_viewset(request, pages_pk=page.pk, pk=tag.pk)

        assert response.status_code == 204
        assert page.tags.all().count() == 0
        assert Tag.objects.all().count() == 1

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_list(self, user: user, page: page, api_factory: APIRequestFactory):
        page.tags.set(baker.make(Tag, _quantity=3))

        request = api_factory.get(f"{self.endpoint}{page.pk}/tags/")
        force_authenticate(request, user=user, token=user.access_token)

        response = list_viewset(request, pages_pk=page.pk)

        assert response.status_code == 200
        assert page.tags.all().count() == 3
        assert Tag.objects.all().count() == 3
        assert TagSerializer(page.tags.all(), many=True).data == response.data
