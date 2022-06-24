import json

from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Page
from .serializers import PageSerializer
from .validators import IsUserOwner, IsUserAdminOrModerator, IsPublicPage
from django.core import serializers


class PageList(generics.ListCreateAPIView):
    serializer_class = PageSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get(self, request, *args, **kwargs):

        if IsUserAdminOrModerator(request.user):
            pages = serializers.serialize('json', Page.objects.all(),
                                          fields=('uuid', 'description', 'tags', 'owner', 'followers', 'is_private'))

            return HttpResponse(pages, content_type='application/json')

        else:
            return HttpResponse(json.dumps({"detail": "You do not have permission to perform this action."}),
                                content_type='application/json')


class PageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    def get(self, request, *args, **kwargs):
        if IsUserOwner(request.user, kwargs['pk']) or IsUserAdminOrModerator(request.user) or IsPublicPage(
                kwargs['pk']):
            page = serializers.serialize('json', Page.objects.filter(pk=kwargs['pk']),
                                         fields=('email', 'username', 'is_active', 'is_staff', 'role'))

            return HttpResponse(page, content_type='application/json')

        else:
            return HttpResponse(json.dumps({"detail": "This is the private page."}),
                                content_type='application/json')

    def put(self, request, *args, **kwargs):
        if IsUserOwner(request.user, kwargs['pk']) or IsUserAdminOrModerator(request.user):

            serializer = self.serializer_class(Page.objects.get(pk=kwargs['pk']), data=request.data, partial=True)

            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return HttpResponse(json.dumps({"detail": "You do not have permission to perform this action."}),
                                content_type='application/json')

    def delete(self, request, *args, **kwargs):
        if IsUserOwner(request.user, kwargs['pk']) or IsUserAdminOrModerator(request.user):
            page = Page.objects.get(pk=kwargs['pk'])
            page.delete()

            return HttpResponse(json.dumps({"detail": "Deleted."}),
                                content_type='application/json')

        else:
            return HttpResponse(json.dumps({"detail": "You do not have permission to perform this action."}),
                                content_type='application/json')

