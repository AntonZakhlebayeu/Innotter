from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, \
    ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from InnotterUser.roles import Roles
from innotter_like.models import Like
from innotter_like.permissions import IsPublicPage, IsOwner
from innotter_like.serializers import CreateLikeSerializer, RetrieveLikeSerializer, ListLikeSerializer
from innotter_like.services import create_like
from innotter_post.permissions import IsInRoleAdminOrModerator


class LikeMixin(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    GenericViewSet
):

    permission_classes = {
            'create': (IsAuthenticated, (IsPublicPage | IsInRoleAdminOrModerator), ),
            'retrieve': (IsAuthenticated, (IsPublicPage | IsOwner | IsInRoleAdminOrModerator), ),
            'list': (IsAuthenticated, (IsPublicPage | IsOwner | IsInRoleAdminOrModerator), ),
            'destroy': (IsAuthenticated, (IsOwner | IsInRoleAdminOrModerator), ),
    }
    serializer_classes = {
            'create': CreateLikeSerializer,
            'retrieve': RetrieveLikeSerializer,
            'list': ListLikeSerializer,
    }

    def perform_create(self, serializer):
        create_like(
            current_user=self.request.user,
            liked_post=serializer.validated_data.get('post')
        )

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def get_permissions(self):
        permission_classes = self.permission_classes.get(self.action)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.action == 'list' and self.request.user.role == Roles.USER:
            return Like.objects.filter(owner=self.request.user)
        return self.queryset
