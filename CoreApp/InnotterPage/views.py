import json

from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from InnotterTag.serializers import TagSerializer
from .models import Page
from .serializers import PageSerializer
from .permissions import IsInRoleAdminOrModerator, IsPublicPage, IsOwner
from InnotterTag.models import Tag


class PageList(generics.ListCreateAPIView):
    serializer_class = PageSerializer
    permission_classes = (IsAuthenticated, IsInRoleAdminOrModerator)
    queryset = Page.objects.all()

    def perform_create(self, serializer):
        tags = []

        for tag in self.request.data.get('tags', ):
            try:
                Tag.objects.get(name=tag['name']).pk
            except Tag.DoesNotExist:
                tag_serializer = TagSerializer(data={"name": tag['name']})
                tag_serializer.is_valid()
                tag_serializer.save()

            tags.append(Tag.objects.get(name=tag['name']).pk)

        serializer.save(owner=self.request.user, tags=tags)


class PageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = (IsAuthenticated & (IsPublicPage | IsInRoleAdminOrModerator | IsOwner),)

    def put(self, request, *args, **kwargs):
        page = Page.objects.get(pk=kwargs['pk'])

        for tag in request.data.get('tags', ):
            try:
                Tag.objects.get(name=tag['name']).pk
            except Tag.DoesNotExist:
                tag_serializer = TagSerializer(data={"name": tag['name']})
                tag_serializer.is_valid()
                tag_serializer.save()

            page.tags.add(Tag.objects.get(name=tag['name']))

        return JsonResponse(PageSerializer(page).data, safe=False)

    def delete(self, request, *args, **kwargs):
        page = Page.objects.get(pk=kwargs['pk'])
        page.delete()

        return HttpResponse(json.dumps({"detail": "Deleted."}), content_type='application/json')