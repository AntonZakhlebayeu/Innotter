from datetime import datetime

from innotter_page.models import Page
from innotter_page.permissions import IsBlockedPage, IsInStaff, IsOwner, IsPublicPage
from innotter_page.serializers import PageSerializer
from innotter_page.utils import time_converter
from producer import publish
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
            (IsPublicPage | IsOwner | IsInStaff),
            IsBlockedPage,
        ),
        "update": (
            IsAuthenticated,
            (IsInStaff | IsOwner),
            IsBlockedPage,
        ),
        "destroy": (
            IsAuthenticated,
            (IsOwner | IsInStaff),
            IsBlockedPage,
        ),
        "list": (
            IsAuthenticated,
            IsInStaff,
        ),
        "block": (
            IsAuthenticated,
            IsInStaff,
        ),
        "unblock": (
            IsAuthenticated,
            IsInStaff,
        ),
    }

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        publish("page_updated", response.data)
        return response

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        response = super().destroy(request, *args, **kwargs)
        publish("page_deleted", {"pk": pk})
        return response

    @action(
        detail=True,
        methods=["put"],
        permission_classes=(
            {
                "block": (
                    IsAuthenticated,
                    IsInStaff,
                ),
            }
        ),
    )
    def block(self, request, *args, **kwargs):
        page = request.data.get(
            "page",
        )

        page_model = Page.objects.get(pk=kwargs["pk"])
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
        permission_classes=(
            {
                "unblock": (
                    IsAuthenticated,
                    IsInStaff,
                ),
            }
        ),
    )
    def unblock(self, request, *args, **kwargs):
        page = request.data.get(
            "page",
        )

        page_model = Page.objects.get(pk=kwargs["pk"])
        if page.get("permanent_block") is None:
            page_model.unblock_date = datetime.now()
        else:
            page_model.is_permanent_blocked = False

        page_model.save()

        return Response(PageSerializer(page_model).data, status=status.HTTP_200_OK)
