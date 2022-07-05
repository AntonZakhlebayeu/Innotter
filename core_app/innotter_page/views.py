from datetime import datetime

from innotter_page.models import Page
from innotter_page.permissions import (IsBlockedPage, IsInRoleAdminOrModerator,
                                       IsOwner, IsPublicPage)
from innotter_page.serializers import PageSerializer
from innotter_page.utils import time_converter
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core_app.default_mixin import GetPermissionsMixin


class PageList(GetPermissionsMixin, viewsets.ModelViewSet):

    serializer_class = PageSerializer
    queryset = Page.objects.all()
    permission_classes = {
        "create": (IsAuthenticated,),
        "retrieve": (
            IsAuthenticated,
            (IsPublicPage | IsOwner | IsInRoleAdminOrModerator),
            IsBlockedPage,
        ),
        "update": (
            IsAuthenticated,
            (IsInRoleAdminOrModerator | IsOwner),
            IsBlockedPage,
        ),
        "destroy": (
            IsAuthenticated,
            (IsOwner | IsInRoleAdminOrModerator),
            IsBlockedPage,
        ),
        "list": (
            IsAuthenticated,
            IsInRoleAdminOrModerator,
        ),
        "block": (
            IsAuthenticated,
            IsInRoleAdminOrModerator,
        ),
        "unblock": (
            IsAuthenticated,
            IsInRoleAdminOrModerator,
        ),
    }

    @action(
        detail=True,
        methods=["put"],
        permission_classes=[
            IsAuthenticated & IsInRoleAdminOrModerator,
        ],
    )
    def block(self, request, *args, **kwargs):
        page = request.data.get(
            "page",
        )

        page_model = Page.objects.get(uuid=page["uuid"])
        if page.get("permanent_block") is None:
            time = page["block_time"].split()
            page_model.unblock_date = datetime.now() + time_converter(time)
        else:
            page_model.is_permanent_blocked = True

        page_model.save()

        return Response(PageSerializer(page_model).data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["put"],
        permission_classes=[
            IsAuthenticated & IsInRoleAdminOrModerator,
        ],
    )
    def unblock(self, request, *args, **kwargs):
        page = request.data.get(
            "page",
        )

        page_model = Page.objects.get(uuid=page["uuid"])
        if page.get("permanent_block") is None:
            page_model.unblock_date = datetime.now()
        else:
            page_model.is_permanent_blocked = False

        page_model.save()

        return Response(PageSerializer(page_model).data, status=status.HTTP_200_OK)
