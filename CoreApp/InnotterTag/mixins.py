from rest_framework import status, viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.response import Response

from InnotterPage.models import Page
from InnotterTag.models import Tag
from InnotterTag.serializers import TagSerializer


class TagAdministrateMixin(viewsets.GenericViewSet,
                           ListModelMixin,
                           RetrieveModelMixin,
                           DestroyModelMixin):

    def destroy(self, request, *args, **kwargs):
        try:
            tag = Tag.objects.get(pk=kwargs['pk'])
            tag.delete()
        except Tag.DoesNotExist:
            return Response({"detail": "Tag does not exist."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"detail": "Deleted."}, status=status.HTTP_204_NO_CONTENT)


class TagMixin(viewsets.GenericViewSet,
               ListModelMixin,
               CreateModelMixin,
               RetrieveModelMixin,
               DestroyModelMixin):

    def retrieve(self, request, *args, **kwargs):

        try:
            Page.objects.get(pk=kwargs['pk']).tags.get(pk=kwargs['pk_tag'])
        except Tag.DoesNotExist:
            return Response({"detail": "Tag does not exists."}, status=status.HTTP_404_NOT_FOUND)

        tag_data = TagSerializer(Tag.objects.get(pk=kwargs['pk_tag']))

        return Response(tag_data.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):

        try:
            Page.objects.get(pk=kwargs['pk']).tags.get(pk=kwargs['pk_tag'])
        except Tag.DoesNotExist:
            return Response({"detail": "Tag does not exists."}, status=status.HTTP_404_NOT_FOUND)

        Page.objects.get(pk=kwargs['pk']).tags.remove(Tag.objects.get(pk=kwargs['pk_tag']))

        return Response({"detail": "Deleted."}, status=status.HTTP_204_NO_CONTENT)
