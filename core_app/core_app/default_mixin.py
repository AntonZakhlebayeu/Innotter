from rest_framework.permissions import IsAuthenticated


class GetSerializerMixin:
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)


class GetPermissionsMixin:
    def get_permissions(self):
        permission_classes = self.permission_classes.get(self.action, IsAuthenticated)
        return [permission() for permission in permission_classes]
