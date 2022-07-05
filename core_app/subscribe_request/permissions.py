from datetime import datetime

import pytz
from innotter_page.models import Page
from rest_framework.permissions import BasePermission
from subscribe_request.models import SubscribeRequest


class IsBlockedPageCreate(BasePermission):
    def has_permission(self, request, view):
        if Page.objects.get(pk=request.data.get("desired_page")).unblock_date is None:
            return True

        return datetime.now().replace(
            tzinfo=pytz.timezone("US/Eastern")
        ) > Page.objects.get(pk=request.data.get("desired_page")).unblock_date.replace(
            tzinfo=pytz.timezone("US/Eastern")
        )


class IsBlockedPageUpdate(BasePermission):
    def has_permission(self, request, view):
        if (
            SubscribeRequest.objects.get(pk=view.kwargs["pk"]).desired_page.unblock_date
            is None
        ):
            return True

        return datetime.now().replace(
            tzinfo=pytz.timezone("US/Eastern")
        ) > SubscribeRequest.objects.get(pk=view.kwargs["pk"]).unblock_date.replace(
            tzinfo=pytz.timezone("US/Eastern")
        )


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.pk
            == SubscribeRequest.objects.get(pk=view.kwargs["pk"]).desired_page.owner.pk
        )


class IsOwnerToAcceptAllSubscribeRequests(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.pk
            == Page.objects.get(pk=request.data.get("desired_page")).owner.pk
        )
