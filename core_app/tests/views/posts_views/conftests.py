import pytest
from innotter_page.models import Page
from innotter_post.models import Post
from model_bakery import baker


@pytest.fixture()
def post(page: Page):
    return baker.make(Post, page=page)


@pytest.fixture()
def new_post():
    return baker.prepare(Post)


@pytest.fixture()
def expected_json(post: Post):
    return {
        "page": post.page.uuid,
        "content": post.content,
        "reply_to": post.reply_to,
        "created_at": str(post.created_at.isoformat()).replace("+00:00", "Z"),
        "updated_at": str(post.updated_at.isoformat()).replace("+00:00", "Z"),
        "replies": list(post.replies.all().values_list("pk", flat=True)),
    }


@pytest.fixture()
def update_json(new_post: Post):
    return {
        "content": new_post.content,
    }


@pytest.fixture()
def expected_update_json(new_post: Post):
    return {
        "content": new_post.content,
    }
