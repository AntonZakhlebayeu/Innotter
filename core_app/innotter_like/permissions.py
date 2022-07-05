from innotter_post.models import Post
from rest_framework.permissions import BasePermission


class IsPublicPage(BasePermission):
    def has_permission(self, request, view, **kwargs):

        page = Post.objects.get(pk=request.data.get("post")).page
        return not page.is_private or page.followers.contains(request.user)


class IsOwner(BasePermission):
    def has_permission(self, request, view, **kwargs):

        page = Post.objects.get(pk=request.data.get("post")).page
        return page.owner.pk == request.user.pk
