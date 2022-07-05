from rest_framework import status
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from innotter_post.permissions import IsInRoleAdminOrModerator, IsOwner, IsPublicPage, IsBlockedPage
from innotter_post.models import Post
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
        'create': (IsAuthenticated & IsBlockedPage & (IsInRoleAdminOrModerator | IsOwner),),
        'update': (IsAuthenticated & IsBlockedPage & (IsInRoleAdminOrModerator | IsOwner), ),
        'partial_update': (IsAuthenticated & IsBlockedPage & (IsInRoleAdminOrModerator | IsOwner), ),
        'retrieve': (IsAuthenticated & IsBlockedPage & (IsInRoleAdminOrModerator | IsOwner | IsPublicPage), ),
        'list': (IsAuthenticated & IsBlockedPage & (IsInRoleAdminOrModerator | IsOwner | IsPublicPage), ),
        'destroy': (IsAuthenticated & IsBlockedPage & (IsInRoleAdminOrModerator | IsOwner), ),
        'get_all_posts': (IsAuthenticated, IsInRoleAdminOrModerator, IsBlockedPage, )
    }

    def retrieve(self, request, *args, **kwargs):
        if kwargs.get('pk') is None:
            return super(RetrievePostSerializer).retrieve(request, *args, **kwargs)
        else:
            post = Post.objects.filter(pk=kwargs.get('pk')).first()
            if post is None or post.page.pk != kwargs.get('pk_page'):
                return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

            return Response(data=RetrievePostSerializer(Post.objects.get(pk=kwargs.get('pk'))).data,
                            status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        return Response(ListPostSerializer(Post.objects.filter(page=kwargs.get('pk_page')), many=True).data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs.get('pk')).first()
        if post is None or post.page.pk != kwargs.get('pk_page'):
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs.get('pk')).first()
        if post is None or post.page.pk != kwargs.get('pk_page'):
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def get_permissions(self):
        permission_classes = self.permission_classes.get(self.action)
        return [permission() for permission in permission_classes]
