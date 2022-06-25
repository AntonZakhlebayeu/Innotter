import json

from django.http import HttpResponse, JsonResponse
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


class AllTagList(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated, IsInRoleAdminOrModerator,)


class TagsAdministrate(generics.RetrieveDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated, IsInRoleAdminOrModerator,)

    def delete(self, request, *args, **kwargs):
        try:
            tag = Tag.objects.get(pk=kwargs['pk'])
            tag.delete()
        except Tag.DoesNotExist:
            return HttpResponse(json.dumps({"detail": "Tag does not exist."}), content_type='application/json')

        return HttpResponse(json.dumps({"detail": "Deleted."}), content_type='application/json')


class TagList(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated & (IsPublicPage | IsInRoleAdminOrModerator | IsOwner),)

    def perform_create(self, serializer):
        serializer.save()
        page = Page.objects.get(pk=self.kwargs['pk'])
        page.tags.add(Tag.objects.get(name=self.request.data.get('name')))

    def get(self, request, *args, **kwargs):
        page = Page.objects.get(pk=kwargs['pk'])

        tag_data = TagSerializer(data=page.tags.all(), many=True)
        tag_data.is_valid()

        return JsonResponse(tag_data.data, safe=False)


class TagDetail(generics.RetrieveDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated & (IsPublicPage | IsInRoleAdminOrModerator | IsOwner),)

    def get(self, request, *args, **kwargs):

        try:
            Page.objects.get(pk=kwargs['pk']).tags.get(pk=kwargs['pk_tag'])
        except Tag.DoesNotExist:
            return HttpResponse(json.dumps({"detail": "Tag does not exists."}), content_type='application/json')

        tag_data = TagSerializer(Tag.objects.get(pk=kwargs['pk_tag']))

        return JsonResponse(tag_data.data, safe=False)

    def delete(self, request, *args, **kwargs):

        try:
            Page.objects.get(pk=kwargs['pk']).tags.get(pk=kwargs['pk_tag'])
        except Tag.DoesNotExist:
            return HttpResponse(json.dumps({"detail": "Tag does not exists."}), content_type='application/json')

        Page.objects.get(pk=kwargs['pk']).tags.remove(Tag.objects.get(pk=kwargs['pk_tag']))

        return HttpResponse(json.dumps({"detail": "Deleted."}), content_type='application/json')
