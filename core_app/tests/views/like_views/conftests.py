import pytest
from innotter_like.models import Like
from innotter_post.models import Post
from model_bakery import baker
from tests.views.posts_views.conftests import post


@pytest.fixture()
def post(post: Post):
    return baker.make(Like, post=post)
