from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
            return Response({"detail": "Tag does not exist."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"detail": "Deleted."}, status=status.HTTP_204_NO_CONTENT)


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

        return Response(tag_data.data)


class TagDetail(generics.RetrieveDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated & (IsPublicPage | IsInRoleAdminOrModerator | IsOwner),)

    def get(self, request, *args, **kwargs):

        try:
            Page.objects.get(pk=kwargs['pk']).tags.get(pk=kwargs['pk_tag'])
        except Tag.DoesNotExist:
            return Response({"detail": "Tag does not exists."}, status=status.HTTP_404_NOT_FOUND)

        tag_data = TagSerializer(Tag.objects.get(pk=kwargs['pk_tag']))

        return Response(tag_data.data, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):

        try:
            Page.objects.get(pk=kwargs['pk']).tags.get(pk=kwargs['pk_tag'])
        except Tag.DoesNotExist:
            return HttpResponse({"detail": "Tag does not exists."}, status=status.HTTP_404_NOT_FOUND)

        Page.objects.get(pk=kwargs['pk']).tags.remove(Tag.objects.get(pk=kwargs['pk_tag']))

        return Response({"detail": "Deleted."}, status=status.HTTP_204_NO_CONTENT)

