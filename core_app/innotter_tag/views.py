from innotter_page.permissions import IsInRoleAdminOrModerator
from innotter_tag.mixins import TagMixin
from innotter_tag.models import Tag
from innotter_tag.serializers import TagSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated


class TagList(TagMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[
            IsAuthenticated & IsInRoleAdminOrModerator,
        ],
    )
    def get_tag(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @action(
        detail=True,
        methods=["put"],
        permission_classes=[
            IsAuthenticated & IsInRoleAdminOrModerator,
        ],
    )
    def all(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(
        detail=True,
        methods=["delete"],
        permission_classes=[
            IsAuthenticated & IsInRoleAdminOrModerator,
        ],
    )
    def delete_tag(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
