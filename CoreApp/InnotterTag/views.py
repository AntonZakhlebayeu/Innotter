from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from InnotterTag.mixins import TagMixin
from InnotterTag.models import Tag
from InnotterTag.serializers import TagSerializer
from InnotterPage.permissions import IsInRoleAdminOrModerator


class TagList(TagMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated & IsInRoleAdminOrModerator, ])
    def get_tag(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['put'], permission_classes=[IsAuthenticated & IsInRoleAdminOrModerator, ])
    def all(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated & IsInRoleAdminOrModerator, ])
    def delete_tag(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



