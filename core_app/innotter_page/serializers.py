from innotter_page.models import Page
from innotter_tag.serializers import TagPageSerializer
from innotter_user.serializers import UsernameSerializer
from producer import publish
from rest_framework import serializers


class PageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    tags = TagPageSerializer

    class Meta:
        model = Page
        fields = [
            "id",
            "uuid",
            "name",
            "description",
            "tags",
            "owner",
            "followers",
            "is_private",
            "unblock_date",
            "is_permanent_blocked",
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["followers"] = UsernameSerializer(instance.followers.all(), many=True).data
        rep["tags"] = TagPageSerializer(instance.tags.all(), many=True).data
        return rep

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["owner"] = request.user
        if validated_data.get("tags") is None:
            page = Page.objects.create(**validated_data)
        else:
            tags = validated_data.pop("tags")
            page = Page.objects.create(**validated_data)
            page.tags.set(tags)

        publish("page_created", PageSerializer(page).data)

        return page
