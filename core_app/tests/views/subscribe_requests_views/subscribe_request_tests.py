from unittest import mock

import pytest
from innotter_page.models import Page
from innotter_user.models import User
from model_bakery import baker
from rest_framework.test import APIRequestFactory, force_authenticate
from subscribe_request.models import SubscribeRequest
from subscribe_request.serializers import (
    CreateSubscribeRequestSerializer,
    ListSubscribeRequestSerializer,
)
from subscribe_request.views import SubscribeRequestViewSet
from tests.views.conftests import api_factory
from tests.views.page_views.conftests import page
from tests.views.subscribe_requests_views.conftests import (
    expected_json,
    expected_update_json,
    subscribe_request,
)
from tests.views.user_views.conftests import user

pytestmark = pytest.mark.django_db
subscribe_request_viewset = SubscribeRequestViewSet.as_view(
    {"get": "retrieve", "post": "create", "put": "update", "delete": "destroy"}
)
list_viewset = SubscribeRequestViewSet.as_view({"get": "list"})
accept_all_viewset = SubscribeRequestViewSet.as_view(
    {"patch": "accept_subscribe_requests"}
)
accept_page_viewset = SubscribeRequestViewSet.as_view(
    {"patch": "accept_page_subscribe_requests"}
)
get_all_page_subscribe_requests_viewset = SubscribeRequestViewSet.as_view(
    {"patch": "get_all_page_subscribe_requests"}
)
decline_page_subscribe_requests_viewset = SubscribeRequestViewSet.as_view(
    {"delete": "decline_page_subscribe_requests"}
)
delete_users_from_followers_viewset = SubscribeRequestViewSet.as_view(
    {"delete": "delete_users_from_followers"}
)


class TestSubscribeRequestEndpoint:
    endpoint = "api/subscribe_request/"

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_create(self, user: user, api_factory: APIRequestFactory):
        page = baker.make(Page)

        create_json = {
            "desired_page": page.id,
        }

        request = api_factory.post(
            f"{self.endpoint}", create_json, format="json"
        )
        force_authenticate(request, user=user, token=user.access_token)

        response = subscribe_request_viewset(request)

        assert response.status_code == 201
        assert (
            response.data
            == CreateSubscribeRequestSerializer(
                SubscribeRequest.objects.first(), context={"request": request}
            ).data
        )

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_retrieve(
        self,
        user: user,
        subscribe_request: subscribe_request,
        expected_json: expected_json,
        api_factory: APIRequestFactory,
    ):

        request = api_factory.get(f"{self.endpoint}{subscribe_request.pk}")
        force_authenticate(request, user=user, token=user.access_token)

        response = subscribe_request_viewset(request, pk=subscribe_request.pk)

        assert response.status_code == 200
        assert response.data == expected_json

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_accept(
        self,
        user: user,
        subscribe_request: subscribe_request,
        expected_update_json: expected_update_json,
        api_factory: APIRequestFactory,
    ):
        request = api_factory.put(
            f"{self.endpoint}{subscribe_request.pk}",
            expected_update_json,
            format="json",
        )
        force_authenticate(request, user=user, token=user.access_token)

        response = subscribe_request_viewset(request, pk=subscribe_request.pk)

        assert response.status_code == 200
        assert response.data == expected_update_json

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_destroy(
        self,
        user: user,
        subscribe_request: subscribe_request,
        api_factory: APIRequestFactory,
    ):
        request = api_factory.delete(f"{self.endpoint}{subscribe_request.pk}")
        force_authenticate(request, user=user, token=user.access_token)

        response = subscribe_request_viewset(request, pk=subscribe_request.pk)

        assert response.status_code == 204
        assert SubscribeRequest.objects.count() == 0

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_list(
        self, user: user, page: page, api_factory: APIRequestFactory
    ):
        baker.make(
            SubscribeRequest, _quantity=4, desired_page=page, is_accepted=False
        )

        request = api_factory.get(f"{self.endpoint}")
        force_authenticate(request, user=user, token=user.access_token)

        response = list_viewset(request)

        assert response.status_code == 200
        assert len(response.data) == 4
        assert SubscribeRequest.objects.count() == 4

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_accept_all(
        self, user: user, page: page, api_factory: APIRequestFactory
    ):
        baker.make(
            SubscribeRequest, _quantity=4, desired_page=page, is_accepted=False
        )

        request = api_factory.patch(f"{self.endpoint}")
        force_authenticate(request, user=user, token=user.access_token)

        response = accept_all_viewset(request)

        assert response.status_code == 200
        assert SubscribeRequest.objects.filter(is_accepted=True).count() == 4

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_accept_page_subscribe_requests(
        self, user: user, page: page, api_factory: APIRequestFactory
    ):
        baker.make(
            SubscribeRequest, _quantity=4, desired_page=page, is_accepted=False
        )
        baker.make(
            SubscribeRequest,
            _quantity=5,
            desired_page=baker.make(Page),
            is_accepted=False,
        )

        page_json = {"desired_page": page.pk}

        request = api_factory.patch(
            f"{self.endpoint}", page_json, format="json"
        )
        force_authenticate(request, user=user, token=user.access_token)

        response = accept_page_viewset(request)

        assert response.status_code == 200
        assert (
            SubscribeRequest.objects.filter(
                desired_page=page, is_accepted=True
            ).count()
            == 4
        )

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_get_all_page_subscribe_requests(
        self, user: user, page: page, api_factory: APIRequestFactory
    ):
        baker.make(
            SubscribeRequest, _quantity=4, desired_page=page, is_accepted=False
        )
        baker.make(
            SubscribeRequest,
            _quantity=5,
            desired_page=baker.make(Page),
            is_accepted=False,
        )

        page_json = {"desired_page": page.pk}

        request = api_factory.patch(
            f"{self.endpoint}", page_json, format="json"
        )
        force_authenticate(request, user=user, token=user.access_token)

        response = get_all_page_subscribe_requests_viewset(request)

        assert response.status_code == 200
        assert (
            response.data
            == ListSubscribeRequestSerializer(
                SubscribeRequest.objects.filter(desired_page=page), many=True
            ).data
        )

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_decline_subscribe_request(
        self, user: user, page: page, api_factory: APIRequestFactory
    ):
        baker.make(
            SubscribeRequest, _quantity=4, desired_page=page, is_accepted=False
        )
        baker.make(
            SubscribeRequest,
            _quantity=5,
            desired_page=baker.make(Page),
            is_accepted=False,
        )

        page_json = {"desired_page": page.pk}

        request = api_factory.delete(
            f"{self.endpoint}", page_json, format="json"
        )
        force_authenticate(request, user=user, token=user.access_token)

        response = decline_page_subscribe_requests_viewset(request)

        assert response.status_code == 204
        assert SubscribeRequest.objects.all().count() == 5
        assert SubscribeRequest.objects.filter(desired_page=page).count() == 0

    @mock.patch("core_app.settings.SECRET_KEY", "1234567890")
    def test_delete_user_from_followers(
        self, user: user, page: page, api_factory: APIRequestFactory
    ):
        followers = baker.make(User, _quantity=4)
        remove = [follower.pk for follower in followers]
        page.followers.set(followers)

        page_json = {"users": remove, "desired_page": page.pk}

        request = api_factory.delete(
            f"{self.endpoint}", page_json, format="json"
        )
        force_authenticate(request, user=user, token=user.access_token)

        response = delete_users_from_followers_viewset(request)

        assert response.status_code == 204
        assert page.followers.all().count() == 0
