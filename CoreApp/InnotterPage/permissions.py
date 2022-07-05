from datetime import datetime
import pytz

from rest_framework.permissions import BasePermission

from InnotterPage.models import Page
from InnotterUser.roles import Roles


class IsInRoleAdminOrModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Roles.ADMIN or request.user.role == Roles.MODERATOR


class IsOwner(BasePermission):
    def has_permission(self, request, view, **kwargs):
        if view.kwargs.get('pk') is None or Page.objects.filter(pk=view.kwargs['pk']).first() is None:
            return False

        return request.user.pk == Page.objects.get(pk=view.kwargs['pk']).owner_id


class IsPublicPage(BasePermission):
    def has_permission(self, request, view, **kwargs):
        if view.kwargs.get('pk') is None or Page.objects.filter(pk=view.kwargs['pk']).first() is None:
            return False

        page = Page.objects.get(pk=view.kwargs['pk'])
        return not page.is_private or page.followers.contains(request.user)


class IsBlockedPage(BasePermission):
    def has_object_permission(self, request, view, obj):
        return not obj.is_permanent_blocked and \
               obj.is_temporary_blocked()
