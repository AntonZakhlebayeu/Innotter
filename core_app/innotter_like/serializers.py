from innotter_like.models import Like
from innotter_user.serializers import UsernameSerializer
from rest_framework import serializers


class CreateLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            "id",
            "post",
            "owner",
        )

        extra_kwargs = {"owner": {"read_only": True}}

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["owner"] = UsernameSerializer(self.context["request"].user).data
        return rep


class RetrieveLikeSerializer(serializers.ModelSerializer):

    post = serializers.SlugRelatedField(slug_field="content", read_only=True)

    class Meta:
        model = Like
        fields = (
            "id",
            "post",
            "owner",
        )


class ListLikeSerializer(serializers.ModelSerializer):

    post = serializers.SlugRelatedField(slug_field="content", read_only=True)

    class Meta:
        model = Like
        fields = (
            "id",
            "post",
            "owner",
        )
