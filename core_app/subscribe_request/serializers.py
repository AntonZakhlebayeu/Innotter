from innotter_tag.serializers import ForTagPageSerializer
from innotter_user.models import User
from innotter_user.serializers import UsernameSerializer
from rest_framework import serializers
from subscribe_request.models import SubscribeRequest


class CreateSubscribeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribeRequest
        fields = [
            "initiator_user",
            "desired_page",
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["initiator_user"] = UsernameSerializer(self.context["request"].user).data
        return rep


class UpdateSubscribeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribeRequest
        fields = ("is_accepted",)


class RetrieveSubscribeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribeRequest
        fields = (
            "id",
            "initiator_user",
            "desired_page",
            "is_accepted",
        )


class ListSubscribeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribeRequest
        fields = (
            "id",
            "initiator_user",
            "desired_page",
            "is_accepted",
        )
