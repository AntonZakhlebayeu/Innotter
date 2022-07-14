from innotter_post.mixins import PostMixin
from innotter_post.models import Post
from innotter_post.permissions import IsInRoleAdminOrModerator
from innotter_post.serializers import ListPostSerializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class PostViewSet(PostMixin):
    queryset = Post.objects.all()


class AllPostViewSet(GenericViewSet, ListModelMixin):
    queryset = Post.objects.all()
    permission_classes = [
        IsAuthenticated,
        IsInRoleAdminOrModerator,
    ]
    serializer_class = ListPostSerializer

    @action(
        detail=False,
        methods=("get",),
    )
    def get_all_posts(self, request):
        data = ListPostSerializer(data=Post.objects.all(), many=True)
        data.is_valid()
        return Response(data=data.data, status=status.HTTP_200_OK)
