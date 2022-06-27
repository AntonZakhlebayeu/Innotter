from rest_framework.permissions import IsAuthenticated

from InnotterTag.mixins import TagAdministrateMixin, TagMixin
from InnotterTag.models import Tag
from InnotterTag.serializers import TagSerializer
from InnotterPage.permissions import IsInRoleAdminOrModerator, IsOwner, IsPublicPage


class AllTagList(TagAdministrateMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated, IsInRoleAdminOrModerator,)


class TagList(TagMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated & (IsPublicPage | IsInRoleAdminOrModerator | IsOwner),)


