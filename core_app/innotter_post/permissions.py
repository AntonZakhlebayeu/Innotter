from innotter_page.models import Page
from innotter_user.roles import Roles
from rest_framework.permissions import BasePermission


class IsInRoleAdminOrModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Roles.ADMIN or request.user.role == Roles.MODERATOR


class IsOwner(BasePermission):
    def has_permission(self, request, view, **kwargs):
        return request.user.pk == Page.objects.get(pk=view.kwargs["pages_pk"]).owner_id


class IsPublicPage(BasePermission):
    def has_permission(self, request, view, **kwargs):
        if request.method == "GET":
            page = Page.objects.get(pk=view.kwargs["pages_pk"])
            return not page.is_private or page.followers.contains(request.user)
        else:
            return False


class IsBlockedPage(BasePermission):
    def has_object_permission(self, request, view, obj):
        return not obj.page.is_permanent_blocked and obj.page.is_temporary_blocked()
