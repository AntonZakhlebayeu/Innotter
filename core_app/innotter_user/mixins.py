from rest_framework import viewsets
from rest_framework.mixins import (
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)


class UserMixin(
    viewsets.GenericViewSet,
    ListModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
):
    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)
