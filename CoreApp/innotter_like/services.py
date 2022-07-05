from InnotterUser.models import User
from innotter_like.models import Like
from innotter_post.models import Post


def create_like(current_user: User, liked_post: Post) -> None:

    if not Like.objects.filter(owner=current_user, post__id=liked_post.id).exists() and \
            not liked_post.page.is_permanent_blocked and \
            liked_post.page.is_temporary_blocked():
        Like.objects.create(owner=current_user, post=liked_post)
    elif Like.objects.filter(owner=current_user, post__id=liked_post.id).exists():
        Like.objects.filter(owner=current_user, post__id=liked_post.id).delete()
