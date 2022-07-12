from innotter_page.models import Page
from innotter_post.models import Post
from innotter_post.tasks import send_email_to_followers_task
from producer import publish
from rest_framework import serializers

from core_app.celery import error_handler


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["content", "reply_to", "created_at", "updated_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        kwargs = request.parser_context["kwargs"]
        page = Page.objects.get(pk=kwargs["pages_pk"])
        validated_data["page"] = page

        post = Post.objects.create(**validated_data)

        emails = [user.email for user in page.followers.all()]

        send_email_to_followers_task.apply_async(
            kwargs={"emails": emails, "page_name": page.name},
            link_error=error_handler.s(),
            retry=True,
            retry_policy={
                "max_retries": 5,
                "interval_start": 0,
                "interval_step": 0.2,
                "interval_max": 0.2,
            },
        )

        publish("post_created", page.pk)

        return post


class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["content"]


class RetrievePostSerializer(serializers.ModelSerializer):
    page = serializers.ReadOnlyField(source="page.uuid")

    class Meta:
        model = Post
        fields = [
            "page",
            "content",
            "reply_to",
            "created_at",
            "updated_at",
            "replies",
        ]


class ListPostSerializer(serializers.ModelSerializer):
    page = serializers.ReadOnlyField(source="page.uuid")

    class Meta:
        model = Post
        fields = [
            "page",
            "content",
            "reply_to",
            "created_at",
            "updated_at",
            "replies",
        ]
