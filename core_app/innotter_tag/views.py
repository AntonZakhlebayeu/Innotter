from innotter_tag.mixins import TagMixin
from innotter_tag.models import Tag
from innotter_tag.serializers import TagSerializer


class TagList(TagMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
