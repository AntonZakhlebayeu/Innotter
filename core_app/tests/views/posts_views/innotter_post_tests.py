from unittest import mock

import pytest
from innotter_page.models import Page
from innotter_post.models import Post
from innotter_post.serializers import CreatePostSerializer
from innotter_post.views import AllPostViewSet, PostViewSet
from model_bakery import baker
from rest_framework.test import APIRequestFactory, force_authenticate
from tests.views.conftests import api_factory
from tests.views.page_views.conftests import page
from tests.views.posts_views.conftests import (
    expected_json,
    expected_update_json,
    new_post,
    post,
    update_json,
)
from tests.views.user_views.conftests import user

pytestmark = pytest.mark.django_db
post_viewset = PostViewSet.as_view(
    {"get": "retrieve", "post": "create", "put": "update", "delete": "destroy"}
)
list_viewset = PostViewSet.as_view({"get": "list"})
get_all_viewsets = AllPostViewSet.as_view({"get": "list"})


class TestPostEndpoint:
    endpoint = "api/pages/"

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_create(
        self,
        user: user,
        page: page,
        new_post: new_post,
        api_factory: APIRequestFactory,
    ):
        post_json = {
            "content": new_post.content,
        }

        request = api_factory.post(
            f"{self.endpoint}{page.pk}/posts/", post_json, format="json"
        )
        force_authenticate(request, user=user, token=user.access_token)

        response = post_viewset(request, pages_pk=page.pk)

        assert response.status_code == 201
        assert response.data == CreatePostSerializer(Post.objects.first()).data

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_retrieve(
        self,
        user: user,
        page: page,
        post: post,
        expected_json: expected_json,
        api_factory: APIRequestFactory,
    ):
        request = api_factory.get(f"{self.endpoint}{page.pk}/posts/{post.pk}/")
        force_authenticate(request, user=user, token=user.access_token)

        response = post_viewset(request, pages_pk=page.pk, pk=post.pk)

        assert response.status_code == 200
        assert response.data == expected_json

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_update(
        self,
        user: user,
        page: page,
        post: post,
        update_json: update_json,
        expected_update_json: expected_update_json,
        api_factory: APIRequestFactory,
    ):
        request = api_factory.put(
            f"{self.endpoint}{page.pk}/posts/{post.pk}/",
            update_json,
            format="json",
        )
        force_authenticate(request, user=user, token=user.access_token)

        response = post_viewset(request, pages_pk=page.pk, pk=post.pk)

        assert response.status_code == 200
        assert response.data == expected_update_json

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_destroy(
        self,
        user: user,
        page: page,
        post: post,
        api_factory: APIRequestFactory,
    ):
        request = api_factory.delete(f"{self.endpoint}{page.pk}/posts/{post.pk}/")
        force_authenticate(request, user=user, token=user.access_token)

        response = post_viewset(request, pages_pk=page.pk, pk=post.pk)

        assert response.status_code == 204
        assert Post.objects.all().count() == 0

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_list(self, user: user, page: page, api_factory: APIRequestFactory):
        baker.make(Post, page=page, _quantity=4)

        request = api_factory.get(f"{self.endpoint}{page.pk}/posts/")
        force_authenticate(request, user=user, token=user.access_token)

        response = list_viewset(request, pages_pk=page.pk)

        assert response.status_code == 200
        assert len(response.data) == 4
        assert len(response.data) == page.posts.all().count()
        assert Post.objects.all().count() == len(response.data)

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_get_all_posts(self, user: user, page: page, api_factory: APIRequestFactory):
        baker.make(Post, page=page, _quantity=3)

        new_page = baker.make(Page)
        baker.make(Post, page=new_page, _quantity=4)

        request = api_factory.get("/api/posts/")
        force_authenticate(request, user=user, token=user.access_token)

        response = get_all_viewsets(request)

        assert response.status_code == 200
        assert len(response.data) == 7
        assert len(response.data) == Post.objects.all().count()
