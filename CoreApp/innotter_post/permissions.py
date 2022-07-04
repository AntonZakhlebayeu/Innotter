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

        print(request.user.pk)
        print(Page.objects.get(pk=view.kwargs['pk_page']).owner_id)
        print(request.user.pk == Page.objects.get(pk=view.kwargs['pk_page']).owner_id)
        return request.user.pk == Page.objects.get(pk=view.kwargs['pk_page']).owner_id


class IsPublicPage(BasePermission):
    def has_permission(self, request, view, **kwargs):
        if request.method == "GET":
            page = Page.objects.get(pk=view.kwargs['pk_page'])
            return not page.is_private or page.followers.contains(request.user)
        else:
            return False
