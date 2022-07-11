import pytest
from innotter_page.models import Page
from innotter_tag.models import Tag
from model_bakery import baker
from tests.views.page_views.conftests import page


@pytest.fixture()
def tag(page: page):
    tag = baker.make(Tag)
    tag.pages.add(page)
    return tag
