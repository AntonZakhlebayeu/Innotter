from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from innotter_post.serializers import CreatePostSerializer, UpdatePostSerializer, RetrievePostSerializer, \
    ListPostSerializer


class PostMixin(GenericViewSet,
                ListModelMixin,
                CreateModelMixin,
                RetrieveModelMixin,
                UpdateModelMixin,
                DestroyModelMixin):

    serializer_classes = {
        'create': CreatePostSerializer,
        'update': UpdatePostSerializer,
        'partial_update': UpdatePostSerializer,
        'retrieve': RetrievePostSerializer,
        'list': ListPostSerializer,
    }

    permission_classes = {
        'create': (IsAuthenticated, ),
        'update': (IsAuthenticated, ),
        'partial_update': (IsAuthenticated, ),
        'retrieve': (IsAuthenticated, ),
        'list': (IsAuthenticated, ),
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def get_permissions(self):
        permission_classes = self.permission_classes.get(self.action)
        return [permission() for permission in permission_classes]