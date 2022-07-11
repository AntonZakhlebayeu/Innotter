import pytest
from innotter_page.models import Page
from innotter_user.models import User
from model_bakery import baker
from subscribe_request.models import SubscribeRequest
from tests.views.user_views.conftests import user


@pytest.fixture()
def subscribe_request(page: Page, user: User):
    return baker.make(
        SubscribeRequest,
        desired_page=page,
        initiator_user=user,
        is_accepted=False,
    )


@pytest.fixture()
def expected_json(subscribe_request: SubscribeRequest):
    return {
        "id": subscribe_request.pk,
        "initiator_user": subscribe_request.initiator_user.pk,
        "desired_page": subscribe_request.desired_page.pk,
        "is_accepted": subscribe_request.is_accepted,
    }


@pytest.fixture()
def expected_update_json():
    return {"is_accepted": True}
