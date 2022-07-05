from django.db import models
from innotter_page.models import Page


class Post(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=180)
    reply_to = models.ForeignKey(
        "Post", on_delete=models.SET_NULL, null=True, related_name="replies"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
