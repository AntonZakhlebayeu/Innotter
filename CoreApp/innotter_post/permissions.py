from rest_framework.permissions import BasePermission

from InnotterPage.models import Page
from InnotterUser.roles import Roles


class IsInRoleAdminOrModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Roles.ADMIN or request.user.role == Roles.MODERATOR


class IsOwner(BasePermission):
    def has_permission(self, request, view, **kwargs):
        if request.method == 'POST':
            return request.user.pk == Page.objects.get(pk=view.kwargs['pk']).owner_id

        return request.user.pk == Page.objects.get(pk=view.kwargs['pk_page']).owner_id


class IsPublicPage(BasePermission):
    def has_permission(self, request, view, **kwargs):
        if request.method == "GET":
            page = Page.objects.get(pk=view.kwargs['pk_page'])
            return not page.is_private or page.followers.contains(request.user)
        else:
            return False


class IsBlockedPage(BasePermission):
    def has_object_permission(self, request, view, obj):
        return not obj.page.is_permanent_blocked and \
               obj.page.check_temporary_block()
