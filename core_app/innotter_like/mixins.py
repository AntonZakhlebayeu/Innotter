from innotter_like.models import Like
from innotter_like.permissions import IsBlockedPage, IsOwner, IsPublicPage
from innotter_like.serializers import (
    CreateLikeSerializer,
    ListLikeSerializer,
    RetrieveLikeSerializer,
)
from innotter_like.services import create_like, delete_like
from innotter_post.models import Post
from innotter_post.permissions import IsInRoleAdminOrModerator
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
            IsInRoleAdminOrModerator,
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
            owner=self.request.user,
            post__id=serializer.validated_data.get("post").pk,
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
        if self.request.data.get("post") is not None:
            return Like.objects.filter(
                post=Post.objects.get(pk=self.request.data.get("post"))
            )
        elif (
            self.request.user.role == Roles.ADMIN
            and self.request.data.get("post") is None
        ):
            return Like.objects.all()
