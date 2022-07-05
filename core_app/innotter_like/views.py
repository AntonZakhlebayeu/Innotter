from innotter_like.mixins import LikeMixin
from innotter_like.models import Like


class LikeViewSet(LikeMixin):
    queryset = Like.objects.all()
