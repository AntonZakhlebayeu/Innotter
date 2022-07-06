from innotter_page.models import Page
from innotter_page.permissions import (
    IsBlockedPage,
    IsInStaff,
    IsOwner,
    IsPublicPage,
)
from innotter_tag.models import Tag
from innotter_tag.serializers import TagSerializer
from rest_framework import status, viewsets
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core_app.default_mixin import GetPermissionsMixin


class TagMixin(
    GetPermissionsMixin,
    viewsets.GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
):

    permission_classes = {
        "create": (
            IsAuthenticated,
            (IsOwner | IsInStaff),
            IsBlockedPage,
        ),
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
        "partial_update": (
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
            (IsPublicPage | IsOwner | IsInStaff),
            IsBlockedPage,
        ),
    }

    def retrieve(self, request, *args, **kwargs):
        if kwargs.get("pk") is None:
            return super().retrieve(request, *args, **kwargs)

        if (
            Page.objects.filter(pk=kwargs["pages_pk"])
            .first()
            .tags.filter(pk=kwargs["pk"])
            .first()
            is None
        ):
            return Response(
                {"detail": "Tag does not exists."},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            Page.objects.get(pk=kwargs["pages_pk"]).tags.get(pk=kwargs["pk"])

        tag_data = TagSerializer(Tag.objects.get(pk=kwargs["pk"]))

        return Response(tag_data.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        if kwargs.get("pk") is None:
            return super().list(request, *args, **kwargs)

        if Page.objects.filter(pk=kwargs["pages_pk"]).first() is None:
            return Response(
                {"detail": "Page does not exists."},
                status=status.HTTP_404_NOT_FOUND,
            )

        tag_data = TagSerializer(
            data=Page.objects.get(pk=kwargs["pages_pk"]).tags, many=True
        )
        tag_data.is_valid()

        return Response(tag_data.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        if kwargs.get("pk") is None:
            return super().destroy(request, *args, **kwargs)

        if (
            Page.objects.filter(pk=kwargs["pages_pk"])
            .first()
            .tags.filter(pk=kwargs["pk"])
            .first()
            is None
        ):
            return Response(
                {"detail": "Tag does not exists."},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            Page.objects.get(pk=kwargs["pages_pk"]).tags.get(pk=kwargs["pk"])

        Page.objects.get(pk=kwargs["pages_pk"]).tags.remove(
            Tag.objects.get(pk=kwargs["pk"])
        )

        return Response(
            {"detail": "Deleted."}, status=status.HTTP_204_NO_CONTENT
        )
