from rest_framework.permissions import BasePermission
from .models import Page


class IsInRoleAdminOrModerator(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        else:
            return request.user.role == 'admin' or request.user.role == 'moderator'

    @property
    def message(self):
        return "A"


class IsOwner(BasePermission):
    def has_permission(self, request, view, **kwargs):
        return request.user.pk == Page.objects.get(pk=view.kwargs['pk']).owner_id

    @property
    def message(self):
        return "B"


class IsPublicPage(BasePermission):
    def has_permission(self, request, view, **kwargs):
        if request.method == "GET":
            return not Page.objects.get(pk=view.kwargs['pk']).is_private
        else:
            return False

    @property
    def message(self):
        return "C"