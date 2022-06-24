import json

from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Page, Tag
from .serializers import PageSerializer, TagSerializer
from django.core import serializers
from .permissions import IsInRoleAdminOrModerator, IsPublicPage, IsOwner


class PageList(generics.ListCreateAPIView):
    serializer_class = PageSerializer
    permission_classes = (IsAuthenticated, IsInRoleAdminOrModerator)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        pages = serializers.serialize('json', Page.objects.all(),
                                      fields=(
                                      'uuid', 'name', 'description', 'tags', 'owner', 'followers', 'is_private'))

        return HttpResponse(pages, content_type='application/json')


class PageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = (IsAuthenticated & (IsPublicPage | IsInRoleAdminOrModerator | IsOwner),)

    def get(self, request, *args, **kwargs):
        page = serializers.serialize('json', Page.objects.filter(pk=kwargs['pk']),
                                     fields=('uuid', 'name', 'description', 'tags', 'owner', 'followers', 'is_private'))

        return HttpResponse(page, content_type='application/json')

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(Page.objects.get(pk=kwargs['pk']), data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        page = Page.objects.get(pk=kwargs['pk'])
        page.delete()

        return HttpResponse(json.dumps({"detail": "Deleted."}), content_type='application/json')


class TagList(generics.ListCreateAPIView):
    pass


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    pass
