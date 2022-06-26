import json

from django.http import HttpResponse, JsonResponse
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import datetime, timedelta

from InnotterTag.serializers import TagSerializer
from .models import Page
from .serializers import PageSerializer
from .permissions import IsInRoleAdminOrModerator, IsPublicPage, IsOwner, IsBlockPage
from InnotterTag.models import Tag


def time_converter(time: list):
    int_time = int(time[1])

    time_dict = {
        'minutes': timedelta(minutes=int_time),
        'hours': timedelta(hours=int_time),
        'days': timedelta(days=int_time)
    }

    return time_dict[time[0].lower()]


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
    permission_classes = (IsAuthenticated & (IsPublicPage | IsInRoleAdminOrModerator | IsOwner) & IsBlockPage,)

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


class PageBlocking(generics.CreateAPIView):
    serializer_class = PageSerializer
    permission_classes = (IsAuthenticated, IsInRoleAdminOrModerator,)

    def post(self, request, *args, **kwargs):
        page = request.data.get('page', )

        page_model = Page.objects.get(uuid=page['uuid'])
        time = page['block_time'].split()
        page_model.unblock_date = datetime.now() + time_converter(time)

        page_model.save()

        return Response(PageSerializer(page_model).data, status=status.HTTP_200_OK)


class PageUnblocking(generics.CreateAPIView):
    serializer_class = PageSerializer
    permission_classes = (IsAuthenticated, IsInRoleAdminOrModerator,)

    def post(self, request, *args, **kwargs):
        page = request.data.get('page', )

        page_model = Page.objects.get(uuid=page['uuid'])

        page_model.unblock_date = datetime.now()
        page_model.save()

        return Response(PageSerializer(page_model).data, status=status.HTTP_200_OK)
