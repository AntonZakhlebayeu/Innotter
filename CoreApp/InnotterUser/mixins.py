from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin


class UserMixin(viewsets.GenericViewSet,
                ListModelMixin,
                UpdateModelMixin,
                RetrieveModelMixin):

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

