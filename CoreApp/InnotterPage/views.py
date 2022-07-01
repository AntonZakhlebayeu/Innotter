from rest_framework import generics, status, viewsets

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import datetime, timedelta

from InnotterPage.models import Page
from InnotterPage.serializers import PageSerializer
from InnotterPage.permissions import IsInRoleAdminOrModerator, IsPublicPage, IsOwner, IsBlockedPage


def time_converter(time: list):
    int_time = int(time[1])

    time_dict = {
        'minutes': timedelta(minutes=int_time),
        'hours': timedelta(hours=int_time),
        'days': timedelta(days=int_time)
    }

    return time_dict[time[0].lower()]


class PageList(viewsets.ModelViewSet):
    serializer_class = PageSerializer
    permission_classes = (IsAuthenticated & (IsInRoleAdminOrModerator | IsPublicPage | IsOwner) & IsBlockedPage, )
    queryset = Page.objects.all()


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
