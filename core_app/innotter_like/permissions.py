from innotter_like.models import Like
from innotter_post.models import Post
from rest_framework.permissions import BasePermission


class IsPublicPage(BasePermission):
    def has_permission(self, request, view, **kwargs):
        if request.method != "POST":
            page = Like.objects.get(pk=view.kwargs["pk"]).post.page
            return not page.is_private or page.followers.contains(request.user)
        return not Post.objects.get(
            pk=request.data.get("post")
        ).page.is_private or Post.objects.get(
            pk=request.data.get("post")
        ).page.followers.contains(
            request.user
        )


class IsOwner(BasePermission):
    def has_permission(self, request, view, **kwargs):
        if view.kwargs.get("pk") is None:
            page = Like.objects.get(pk=view.kwargs["pk"]).post.page
            return page.owner.pk == request.user.pk
        page = Post.objects.get(pk=request.data.get("post")).page
        return page.owner.pk == request.user.pk


class IsBlockedPage(BasePermission):
    def has_permission(self, request, view):
        if request.method != "POST":
            page = Like.objects.get(pk=view.kwargs["pk"]).post.page
            return (
                not page.is_permanent_blocked and page.is_temporary_blocked()
            )
        return (
            not Post.objects.get(
                pk=request.data.get("post")
            ).page.is_permanent_blocked
            and Post.objects.get(
                pk=request.data.get("post")
            ).page.is_temporary_blocked()
        )
