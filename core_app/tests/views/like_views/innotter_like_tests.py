from unittest import mock

import pytest
from innotter_like.models import Like
from innotter_like.serializers import (
    CreateLikeSerializer,
    RetrieveLikeSerializer,
)
from innotter_like.views import LikeViewSet
from model_bakery import baker
from rest_framework.test import APIRequestFactory, force_authenticate
from tests.views.conftests import api_factory
from tests.views.page_views.conftests import page
from tests.views.posts_views.conftests import post
from tests.views.user_views.conftests import user

like_viewset = LikeViewSet.as_view(
    {"get": "retrieve", "post": "create", "delete": "destroy"}
)
list_viewset = LikeViewSet.as_view({"get": "list"})
pytestmark = pytest.mark.django_db


class TestLikeEndpoint:
    endpoint = "/api/likes/"

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_create(
        self, user: user, post: post, api_factory: APIRequestFactory
    ):
        like_json = {"post": post.pk}

        request = api_factory.post(self.endpoint, like_json, format="json")
        force_authenticate(request, user=user, token=user.access_token)

        response = like_viewset(request)
        like = CreateLikeSerializer(
            Like.objects.first(), context={"request": request}
        ).data
        like.pop("id")

        assert response.status_code == 201
        assert Like.objects.count() == 1
        assert response.data == like

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_create_if_exists(
        self, user: user, post: post, api_factory: APIRequestFactory
    ):
        baker.make(Like, owner=user, post=post)
        like_json = {"post": post.pk}

        request = api_factory.post(self.endpoint, like_json, format="json")
        force_authenticate(request, user=user, token=user.access_token)

        response = like_viewset(request)

        assert response.status_code == 201
        assert Like.objects.count() == 0

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_retrieve(
        self, user: user, post: post, api_factory: APIRequestFactory
    ):
        like = baker.make(Like, owner=user, post=post)

        request = api_factory.get(
            f"{self.endpoint}{like.pk}", {"post": post.pk}, format="json"
        )
        force_authenticate(request, user=user, token=user.access_token)

        response = like_viewset(request, pk=like.pk)

        assert response.status_code == 200
        assert response.data == RetrieveLikeSerializer(like).data

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_destroy(
        self, user: user, post: post, api_factory: APIRequestFactory
    ):
        like = baker.make(Like, owner=user, post=post)

        request = api_factory.delete(
            f"{self.endpoint}{like.pk}", {"post": post.pk}, format="json"
        )
        force_authenticate(request, user=user, token=user.access_token)

        response = like_viewset(request, pk=like.pk)

        assert response.status_code == 204
        assert Like.objects.all().count() == 0

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_list(self, user: user, api_factory: APIRequestFactory):
        baker.make(Like, _quantity=4)

        request = api_factory.get(f"{self.endpoint}", format="json")
        force_authenticate(request, user=user, token=user.access_token)

        response = list_viewset(request)

        assert response.status_code == 200
        assert Like.objects.all().count() == 4
