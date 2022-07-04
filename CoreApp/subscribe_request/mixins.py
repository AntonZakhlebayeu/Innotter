from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)

from InnotterPage.permissions import IsInRoleAdminOrModerator
from InnotterUser.roles import Roles

from subscribe_request.models import SubscribeRequest
from subscribe_request.permissions import IsBlockedPageCreate, IsBlockedPageUpdate, IsOwner, IsOwnerToAcceptAllSubscribeRequests
from subscribe_request.serializers import (
    CreateSubscribeRequestSerializer,
    RetrieveSubscribeRequestSerializer,
    UpdateSubscribeRequestSerializer,
    ListSubscribeRequestSerializer,
)
from subscribe_request.services import create_subscribe_request, update_subscribe_request


class SubscribeRequestMixin(
        CreateModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin,
        DestroyModelMixin,
        ListModelMixin,
        GenericViewSet
        ):

    serializer_classes = {
            'create': CreateSubscribeRequestSerializer,
            'update': UpdateSubscribeRequestSerializer,
            'partial_update': UpdateSubscribeRequestSerializer,
            'retrieve': RetrieveSubscribeRequestSerializer,
            'list': ListSubscribeRequestSerializer,
    }

    permission_classes = {
        'create': (IsAuthenticated, IsBlockedPageCreate, ),
        'update': (IsAuthenticated, (IsInRoleAdminOrModerator | IsOwner), IsBlockedPageUpdate, ),
        'partial_update': (IsAuthenticated, (IsInRoleAdminOrModerator | IsOwner), IsBlockedPageUpdate, ),
        'retrieve': (IsAuthenticated, (IsInRoleAdminOrModerator | IsOwner), IsBlockedPageUpdate, ),
        'list': (IsAuthenticated, IsInRoleAdminOrModerator, ),
        'destroy': (IsAuthenticated, (IsInRoleAdminOrModerator | IsOwnerToAcceptAllSubscribeRequests), ),
        'accept_subscribe_requests': (IsAuthenticated, IsInRoleAdminOrModerator, ),
        'accept_page_subscribe_requests': (IsAuthenticated, (IsInRoleAdminOrModerator | IsOwnerToAcceptAllSubscribeRequests),),
        'delete_users_from_followers': (IsAuthenticated, (IsInRoleAdminOrModerator | IsOwnerToAcceptAllSubscribeRequests),),
        'decline_page_subscribe_requests': (IsAuthenticated, (IsInRoleAdminOrModerator | IsOwnerToAcceptAllSubscribeRequests),),
    }

    def perform_create(self, serializer):
        create_subscribe_request(
            initiator_user=self.request.user,
            desired_page=serializer.validated_data.get('desired_page')
        )

    def perform_update(self, serializer):
        updating_page = self.get_object()
        update_subscribe_request(
            initiator_user=updating_page.initiator_user,
            desired_page=updating_page.desired_page,
            is_accepted=serializer.validated_data.get('is_accepted')
        )

        serializer.save()

    def get_queryset(self):
        user_role = self.request.user.role
        if self.action == 'list' and user_role == Roles.ADMIN:
            return SubscribeRequest.objects.filter(
                Q(initiator_user=self.request.user) |
                Q(desired_page__owner=self.request.user)
            )
        if self.action == 'accept_subscribe_requests' and user_role == Roles.ADMIN:
            return SubscribeRequest.objects.filter(
                Q(desired_page__owner=self.request.user) &
                Q(is_accepted=False)
            )
        return self.queryset

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def get_permissions(self):
        permission_classes = self.permission_classes.get(self.action)
        return [permission() for permission in permission_classes]
