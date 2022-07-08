import pytest
from innotter_page.models import Page
from innotter_tag.serializers import TagSerializer
from innotter_user.models import User
from innotter_user.serializers import UsernameSerializer
from model_bakery import baker
from tests.views.user_views.conftests import user


@pytest.fixture()
def page(user: User):
    return baker.make(Page)


@pytest.fixture()
def new_page():
    return baker.prepare(Page)


@pytest.fixture()
def expected_json(page: Page):
    return {
        "uuid": page.uuid,
        "name": page.name,
        "description": page.description,
        "tags": TagSerializer(page.tags.all(), many=True).data,
        "owner": page.owner.username,
        "followers": UsernameSerializer(page.followers.all(), many=True).data,
        "is_private": page.is_private,
        "unblock_date": page.unblock_date,
        "is_permanent_blocked": page.is_permanent_blocked,
    }


@pytest.fixture()
def update_json(new_page: Page):
    return {
        "uuid": new_page.uuid,
        "name": new_page.name,
        "description": new_page.description,
    }


@pytest.fixture()
def expected_update_json(page: Page, new_page: Page):
    return {
        "uuid": new_page.uuid,
        "name": new_page.name,
        "description": new_page.description,
        "tags": TagSerializer(page.tags.all(), many=True).data,
        "owner": page.owner.username,
        "followers": UsernameSerializer(page.followers.all(), many=True).data,
        "is_private": page.is_private,
        "unblock_date": page.unblock_date,
        "is_permanent_blocked": page.is_permanent_blocked,
    }


@pytest.fixture()
def block_json():
    return {"page": {"block_time": "minutes 5"}}
