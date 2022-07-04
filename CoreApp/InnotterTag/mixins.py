from rest_framework import status, viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin, CreateModelMixin, \
    UpdateModelMixin
from rest_framework.response import Response

from InnotterPage.models import Page
from InnotterTag.models import Tag
from InnotterTag.serializers import TagSerializer


class TagMixin(viewsets.GenericViewSet,
               ListModelMixin,
               CreateModelMixin,
               UpdateModelMixin,
               RetrieveModelMixin,
               DestroyModelMixin):

    def retrieve(self, request, *args, **kwargs):
        if kwargs.get('pk_tag') is None:
            return super().retrieve(request, *args, **kwargs)

        if Page.objects.filter(pk=kwargs['pk']).first().tags.filter(pk=kwargs['pk_tag']).first() is None:
            return Response({"detail": "Tag does not exists."}, status=status.HTTP_404_NOT_FOUND)
        else:
            Page.objects.get(pk=kwargs['pk']).tags.get(pk=kwargs['pk_tag'])

        tag_data = TagSerializer(Tag.objects.get(pk=kwargs['pk_tag']))

        return Response(tag_data.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        if kwargs.get('pk') is None:
            return super().list(request, *args, **kwargs)

        if Page.objects.filter(pk=kwargs['pk']).first() is None:
            return Response({"detail": "Page does not exists."}, status=status.HTTP_404_NOT_FOUND)

        tag_data = TagSerializer(data=Page.objects.get(pk=kwargs['pk']).tags, many=True)
        tag_data.is_valid()

        return Response(tag_data.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        if kwargs.get('pk_tag') is None:
            return super().destroy(request, *args, **kwargs)

        if Page.objects.filter(pk=kwargs['pk']).first().tags.filter(pk=kwargs['pk_tag']).first() is None:
            return Response({"detail": "Tag does not exists."}, status=status.HTTP_404_NOT_FOUND)
        else:
            Page.objects.get(pk=kwargs['pk']).tags.get(pk=kwargs['pk_tag'])

        Page.objects.get(pk=kwargs['pk']).tags.remove(Tag.objects.get(pk=kwargs['pk_tag']))

        return Response({"detail": "Deleted."}, status=status.HTTP_204_NO_CONTENT)
