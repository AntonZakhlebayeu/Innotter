from rest_framework import status, viewsets
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import datetime

from InnotterPage.models import Page
from InnotterPage.serializers import PageSerializer
from InnotterPage.permissions import IsInRoleAdminOrModerator, IsPublicPage, IsOwner, IsBlockedPage
from InnotterPage.utils import time_converter


class PageList(viewsets.ModelViewSet):
    serializer_class = PageSerializer
    permission_classes = (IsAuthenticated, (IsInRoleAdminOrModerator | IsPublicPage | IsOwner), IsBlockedPage, )
    queryset = Page.objects.all()

    @action(detail=True, methods=['put'], permission_classes=[IsAuthenticated & IsInRoleAdminOrModerator, ])
    def block(self, request, *args, **kwargs):
        page = request.data.get('page', )

        page_model = Page.objects.get(uuid=page['uuid'])
        time = page['block_time'].split()
        page_model.unblock_date = datetime.now() + time_converter(time)

        page_model.save()

        return Response(PageSerializer(page_model).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'], permission_classes=[IsAuthenticated & IsInRoleAdminOrModerator, ])
    def unblock(self, request, *args, **kwargs):
        page = request.data.get('page', )

        page_model = Page.objects.get(uuid=page['uuid'])

        page_model.unblock_date = datetime.now()
        page_model.save()

        return Response(PageSerializer(page_model).data, status=status.HTTP_200_OK)
