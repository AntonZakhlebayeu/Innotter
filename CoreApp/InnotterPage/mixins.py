from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin

from rest_framework.response import Response

from InnotterPage.models import Page
from InnotterPage.serializers import PageSerializer
from InnotterTag.models import Tag
from InnotterTag.serializers import TagSerializer


class PageMixin(GenericAPIView,
                ListModelMixin,
                CreateModelMixin,
                RetrieveModelMixin,
                UpdateModelMixin,
                DestroyModelMixin):

    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs['pk']
            return self.retrieve(request, *args, **kwargs)
        except KeyError:
            return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

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

    def update(self, request, *args, **kwargs):
        page = Page.objects.get(pk=kwargs['pk'])

        tags_by_name = request.data.pop('tags', )
        tags_by_id = []

        for tag in tags_by_name:
            try:
                Tag.objects.get(name=tag['name']).pk
            except Tag.DoesNotExist:
                tag_serializer = TagSerializer(data={"name": tag['name']})
                tag_serializer.is_valid()
                tag_serializer.save()

            tags_by_id.append(Tag.objects.get(name=tag['name']).pk)

        request.data['tags'] = tags_by_id

        serializer = self.serializer_class(
            page, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(PageSerializer(page).data)

    def destroy(self, request, *args, **kwargs):
        page = Page.objects.get(pk=kwargs['pk'])
        page.delete()

        return Response({"detail": "Deleted."}, status=status.HTTP_204_NO_CONTENT)
