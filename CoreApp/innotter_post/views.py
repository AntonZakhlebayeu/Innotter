from innotter_post.mixins import PostMixin
from innotter_post.models import Post


class PostViewSet(PostMixin):
    queryset = Post.objects.all()
