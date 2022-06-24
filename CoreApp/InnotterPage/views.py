import json

from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Page, Tag
from .serializers import PageSerializer, TagSerializer
from .permissions import IsInRoleAdminOrModerator, IsPublicPage, IsOwner


class PageList(generics.ListCreateAPIView):
    serializer_class = PageSerializer
    permission_classes = (IsAuthenticated, IsInRoleAdminOrModerator)
    queryset = Page.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = (IsAuthenticated & (IsPublicPage | IsInRoleAdminOrModerator | IsOwner),)

    def delete(self, request, *args, **kwargs):
        page = Page.objects.get(pk=kwargs['pk'])
        page.delete()

        return HttpResponse(json.dumps({"detail": "Deleted."}), content_type='application/json')


class TagList(generics.ListCreateAPIView):
    pass


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    pass
