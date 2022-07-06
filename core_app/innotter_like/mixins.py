from innotter_like.models import Like
from innotter_like.permissions import IsOwner, IsPublicPage
from innotter_like.serializers import (CreateLikeSerializer,
                                       ListLikeSerializer,
                                       RetrieveLikeSerializer)
from innotter_like.services import create_like, delete_like
from innotter_post.permissions import IsBlockedPage, IsInRoleAdminOrModerator
from innotter_user.roles import Roles
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from core_app.default_mixin import GetPermissionsMixin, GetSerializerMixin


class LikeMixin(
    GetSerializerMixin,
    GetPermissionsMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    GenericViewSet,
):

    permission_classes = {
        "create": (
            IsAuthenticated,
            (IsPublicPage | IsInRoleAdminOrModerator),
            IsBlockedPage,
        ),
        "retrieve": (
            IsAuthenticated,
            (IsPublicPage | IsOwner | IsInRoleAdminOrModerator),
            IsBlockedPage,
        ),
        "list": (
            IsAuthenticated,
            (IsPublicPage | IsOwner | IsInRoleAdminOrModerator),
            IsBlockedPage,
        ),
        "destroy": (
            IsAuthenticated,
            (IsOwner | IsInRoleAdminOrModerator),
            IsBlockedPage,
        ),
    }
    serializer_classes = {
        "create": CreateLikeSerializer,
        "retrieve": RetrieveLikeSerializer,
        "list": ListLikeSerializer,
    }

    def perform_create(self, serializer):

        if not Like.objects.filter(
            owner=self.request.user, post__id=serializer.validated_data.get("post").pk
        ).exists():
            create_like(
                current_user=self.request.user,
                liked_post=serializer.validated_data.get("post"),
            )
        else:
            delete_like(
                current_user=self.request.user,
                liked_post=serializer.validated_data.get("post"),
            )

    def get_queryset(self):
        if self.action == "list" and self.request.user.role == Roles.USER:
            return Like.objects.filter(owner=self.request.user)
        return self.queryset
