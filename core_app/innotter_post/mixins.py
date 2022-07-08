from innotter_page.models import Page
from innotter_post.permissions import (
    IsBlockedPage,
    IsInRoleAdminOrModerator,
    IsOwner,
    IsPublicPage,
)
from innotter_post.serializers import (
    CreatePostSerializer,
    ListPostSerializer,
    RetrievePostSerializer,
    UpdatePostSerializer,
)
from rest_framework.exceptions import NotFound
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


class PostMixin(
    GetPermissionsMixin,
    GetSerializerMixin,
    GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):

    serializer_classes = {
        "create": CreatePostSerializer,
        "update": UpdatePostSerializer,
        "partial_update": UpdatePostSerializer,
        "retrieve": RetrievePostSerializer,
        "list": ListPostSerializer,
    }

    permission_classes = {
        "create": (
            IsAuthenticated
            & IsBlockedPage
            & (IsInRoleAdminOrModerator | IsOwner),
        ),
        "update": (
            IsAuthenticated
            & IsBlockedPage
            & (IsInRoleAdminOrModerator | IsOwner),
        ),
        "partial_update": (
            IsAuthenticated
            & IsBlockedPage
            & (IsInRoleAdminOrModerator | IsOwner),
        ),
        "retrieve": (
            IsAuthenticated
            & IsBlockedPage
            & (IsInRoleAdminOrModerator | IsOwner | IsPublicPage),
        ),
        "list": (
            IsAuthenticated
            & IsBlockedPage
            & (IsInRoleAdminOrModerator | IsOwner | IsPublicPage),
        ),
        "destroy": (
            IsAuthenticated
            & IsBlockedPage
            & (IsInRoleAdminOrModerator | IsOwner),
        ),
    }

    def get_queryset(self, *args, **kwargs):
        pages_id = self.kwargs.get("pages_pk")
        try:
            page = Page.objects.get(pk=pages_id)
        except Page.DoesNotExist:
            raise NotFound("A page with this id does not exist")
        return self.queryset.filter(page=page)
