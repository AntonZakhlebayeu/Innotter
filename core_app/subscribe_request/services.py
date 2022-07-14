from typing import Optional

from django.db.models.query import QuerySet
from innotter_page.models import Page
from innotter_user.models import User
from producer import publish
from subscribe_request.models import SubscribeRequest


def accept_all_subscribe_requests(
    queryset_subscribe_requests: QuerySet,
) -> None:
    for subscribe_request in queryset_subscribe_requests:
        subscribe_request.is_accepted = True
        subscribe_request.desired_page.followers.add(subscribe_request.initiator_user)
        subscribe_request.save()
        publish("follower_added", subscribe_request.desired_page.pk)


def create_subscribe_request(
    initiator_user: User, desired_page: Page
) -> Optional[SubscribeRequest]:

    if (
        desired_page.is_private
        and not SubscribeRequest.objects.filter(
            initiator_user=initiator_user, desired_page=desired_page
        ).exists()
    ):
        return SubscribeRequest.objects.create(
            initiator_user=initiator_user, desired_page=desired_page
        )

    elif (
        not desired_page.is_private
        and not SubscribeRequest.objects.filter(
            initiator_user=initiator_user, desired_page=desired_page
        ).exists()
    ):
        desired_page.followers.add(initiator_user)
        publish("follower_added", desired_page.pk)

        subscribe_request = SubscribeRequest.objects.create(
            initiator_user=initiator_user, desired_page=desired_page
        )
        subscribe_request.is_accepted = True
        subscribe_request.save()

        return subscribe_request


def update_subscribe_request(
    initiator_user: User, desired_page: Page, is_accepted: bool
) -> None:
    if is_accepted:
        desired_page.followers.add(initiator_user)
        publish("follower_added", desired_page.pk)
