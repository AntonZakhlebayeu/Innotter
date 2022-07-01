from rest_framework.permissions import BasePermission

from InnotterUser.roles import Roles


class IsInRoleAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Roles.ADMIN
