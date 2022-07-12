from innotter_like.models import Like
from innotter_post.models import Post
from innotter_user.models import User
from producer import publish


def create_like(current_user: User, liked_post: Post) -> None:
    Like.objects.create(owner=current_user, post=liked_post)
    publish("like_created", liked_post.page.pk)


def delete_like(current_user: User, liked_post: Post) -> None:
    Like.objects.filter(owner=current_user, post__id=liked_post.id).delete()
    publish("like_deleted", liked_post.page.pk)
