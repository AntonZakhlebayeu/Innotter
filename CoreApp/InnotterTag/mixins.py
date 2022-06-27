from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.response import Response

from InnotterPage.models import Page
from InnotterTag.models import Tag
from InnotterTag.serializers import TagSerializer


class TagAdministrateMixin(GenericAPIView,
                           ListModelMixin,
                           RetrieveModelMixin,
                           DestroyModelMixin):

    def perform_create(self, serializer):
        serializer.save()
        page = Page.objects.get(pk=self.kwargs['pk'])
        page.tags.add(Tag.objects.get(name=self.request.data.get('name')))

    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs['pk']
            return self.retrieve(request, *args, **kwargs)
        except KeyError:
            return self.list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            tag = Tag.objects.get(pk=kwargs['pk'])
            tag.delete()
        except Tag.DoesNotExist:
            return Response({"detail": "Tag does not exist."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"detail": "Deleted."}, status=status.HTTP_204_NO_CONTENT)


class TagMixin(GenericAPIView,
               ListModelMixin,
               RetrieveModelMixin,
               DestroyModelMixin):

    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs['pk']
            return self.retrieve(request, *args, **kwargs)
        except KeyError:
            return self.list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        try:
            page = Page.objects.get(pk=kwargs['pk'])
        except Page.DoesNotExist:
            return Response({'detail': 'Page does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        tag_data = TagSerializer(data=page.tags.all(), many=True)
        tag_data.is_valid()

        return Response(tag_data.data)

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
