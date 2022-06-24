from rest_framework.permissions import BasePermission

from InnotterUser.models import User


class IsInRoleAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'
