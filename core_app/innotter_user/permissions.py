from innotter_user.roles import Roles
from rest_framework.permissions import BasePermission


class IsInRoleAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Roles.ADMIN
