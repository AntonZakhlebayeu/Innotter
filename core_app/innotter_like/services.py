from innotter_like.models import Like
from innotter_post.models import Post
from innotter_user.models import User


def create_like(current_user: User, liked_post: Post) -> None:
    Like.objects.create(owner=current_user, post=liked_post)


def delete_like(current_user: User, liked_post: Post) -> None:
    Like.objects.filter(owner=current_user, post__id=liked_post.id).delete()
