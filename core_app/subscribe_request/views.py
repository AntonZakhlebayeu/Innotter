from innotter_page.models import Page
from innotter_user.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from subscribe_request.mixins import SubscribeRequestMixin
from subscribe_request.models import SubscribeRequest
from subscribe_request.serializers import (
    ListSubscribeRequestSerializer,
    RetrieveSubscribeRequestSerializer,
)
from subscribe_request.services import accept_all_subscribe_requests


class SubscribeRequestViewSet(SubscribeRequestMixin):
    queryset = SubscribeRequest.objects.all()

    @action(detail=False, methods=("patch",))
    def accept_subscribe_requests(self, request):
        accept_all_subscribe_requests(queryset_subscribe_requests=self.get_queryset())
        return Response(status=HTTP_200_OK)

    @action(detail=False, methods=("get",))
    def get_all_page_subscribe_requests(self, request):
        requests_queryset = SubscribeRequest.objects.filter(
            desired_page=request.data.get("desired_page"), is_accepted=False
        )

        requests = ListSubscribeRequestSerializer(many=True, data=requests_queryset)
        requests.is_valid()

        return Response(data=requests.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=("patch",))
    def accept_page_subscribe_requests(self, request):
        accept_all_subscribe_requests(
            queryset_subscribe_requests=SubscribeRequest.objects.filter(
                desired_page=request.data.get("desired_page"),
                is_accepted=False,
            )
        )
        return Response(status=HTTP_200_OK)

    @action(detail=False, methods=("delete",))
    def decline_page_subscribe_requests(self, request):
        subscribe_requests = SubscribeRequest.objects.filter(
            desired_page=request.data.get(
                "desired_page",
            ),
            is_accepted=False,
        )
        subscribe_requests.delete()

        return Response({"detail": "Declined."}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=("delete",))
    def delete_users_from_followers(self, request):
        users = request.data.get("users")
        page = Page.objects.get(pk=request.data.get("desired_page"))

        for user in users:
            page.followers.remove(user)

        page.save()

        return Response({"detail": "Deleted."}, status=status.HTTP_204_NO_CONTENT)
