import json

from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from InnotterPage.models import Page
from InnotterTag.models import Tag
from InnotterTag.serializers import TagSerializer
from InnotterPage.permissions import IsInRoleAdminOrModerator, IsOwner, IsPublicPage


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

