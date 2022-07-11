from django.db.models import Q
from innotter_page.permissions import IsInStaff
from innotter_user.roles import Roles
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from subscribe_request.models import SubscribeRequest
from subscribe_request.permissions import (
    IsBlockedPageCreate,
    IsBlockedPageUpdate,
    IsOwner,
    IsOwnerToAcceptAllSubscribeRequests,
)
from subscribe_request.serializers import (
    CreateSubscribeRequestSerializer,
    ListSubscribeRequestSerializer,
    RetrieveSubscribeRequestSerializer,
    UpdateSubscribeRequestSerializer,
)
from subscribe_request.services import (
    create_subscribe_request,
    update_subscribe_request,
)

from core_app.default_mixin import GetPermissionsMixin, GetSerializerMixin


class SubscribeRequestMixin(
    GetPermissionsMixin,
    GetSerializerMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    GenericViewSet,
):

    serializer_classes = {
        "create": CreateSubscribeRequestSerializer,
        "update": UpdateSubscribeRequestSerializer,
        "partial_update": UpdateSubscribeRequestSerializer,
        "retrieve": RetrieveSubscribeRequestSerializer,
        "list": ListSubscribeRequestSerializer,
    }

    permission_classes = {
        "create": (
            IsAuthenticated,
            IsBlockedPageCreate,
        ),
        "update": (
            IsAuthenticated,
            (IsInStaff | IsOwner),
            IsBlockedPageUpdate,
        ),
        "partial_update": (
            IsAuthenticated,
            (IsInStaff | IsOwner),
            IsBlockedPageUpdate,
        ),
        "retrieve": (
            IsAuthenticated,
            (IsInStaff | IsOwner),
            IsBlockedPageUpdate,
        ),
        "list": (
            IsAuthenticated,
            IsInStaff,
        ),
        "destroy": (
            IsAuthenticated,
            (IsInStaff | IsOwnerToAcceptAllSubscribeRequests),
        ),
        "accept_subscribe_requests": (
            IsAuthenticated,
            IsInStaff,
        ),
        "accept_page_subscribe_requests": (
            IsAuthenticated
            & (IsInStaff | IsOwnerToAcceptAllSubscribeRequests),
        ),
        "delete_users_from_followers": (
            IsAuthenticated,
            (IsInStaff | IsOwnerToAcceptAllSubscribeRequests),
        ),
        "decline_page_subscribe_requests": (
            IsAuthenticated,
            (IsInStaff | IsOwnerToAcceptAllSubscribeRequests),
        ),
        "get_all_page_subscribe_requests": (
            IsAuthenticated,
            (IsInStaff | IsOwnerToAcceptAllSubscribeRequests),
        ),
    }

    def perform_create(self, serializer):
        create_subscribe_request(
            initiator_user=self.request.user,
            desired_page=serializer.validated_data.get("desired_page"),
        )

    def perform_update(self, serializer):
        updating_page = self.get_object()
        update_subscribe_request(
            initiator_user=updating_page.initiator_user,
            desired_page=updating_page.desired_page,
            is_accepted=serializer.validated_data.get("is_accepted"),
        )

        serializer.save()

    def get_queryset(self):
        user_role = self.request.user.role
        if self.action == "list" and (
            user_role == Roles.ADMIN or user_role == Roles.MODERATOR
        ):
            return SubscribeRequest.objects.all()
        if (
            self.action == "accept_subscribe_requests"
            and user_role == Roles.ADMIN
        ):
            return SubscribeRequest.objects.filter(Q(is_accepted=False))
        return self.queryset
