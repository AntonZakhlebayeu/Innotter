from rest_framework.permissions import BasePermission


class IsInRoleAdminOrModerator(BasePermission):
    def has_permission(self, request, view):

        return True
