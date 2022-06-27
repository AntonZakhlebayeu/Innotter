from datetime import datetime
import pytz

from rest_framework.permissions import BasePermission

from InnotterPage.models import Page


class IsInRoleAdminOrModerator(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        else:
            return request.user.role == 'admin' or request.user.role == 'moderator'


class IsOwner(BasePermission):
    def has_permission(self, request, view, **kwargs):
        return request.user.pk == Page.objects.get(pk=view.kwargs['pk']).owner_id


class IsPublicPage(BasePermission):
    def has_permission(self, request, view, **kwargs):
        if request.method == "GET":
            return not Page.objects.get(pk=view.kwargs['pk']).is_private
        else:
            return False


class IsBlockedPage(BasePermission):
    def has_permission(self, request, view, **kwargs):
        if request.method == "POST":
            return True

        if Page.objects.get(pk=view.kwargs['pk']).unblock_date is None:
            return True

        if request.user.role == 'admin' or request.user.role == 'moderator':
            return True

        return datetime.now().replace(tzinfo=pytz.timezone('US/Eastern')) > Page.objects.get(pk=view.kwargs['pk']).\
            unblock_date.replace(tzinfo=pytz.timezone('US/Eastern'))
