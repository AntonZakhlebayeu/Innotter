from rest_framework import serializers

from InnotterUser.serializers import UsernameSerializer
from InnotterTag.serializers import TagPageSerializer, TagSerializer
from InnotterPage.models import Page


class PageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    tags = TagPageSerializer

    class Meta:
        model = Page
        fields = ['uuid', 'name', 'description', 'tags', 'owner', 'followers', 'is_private', 'unblock_date']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["followers"] = UsernameSerializer(instance.followers.all(), many=True).data
        rep['tags'] = TagPageSerializer(instance.tags.all(), many=True).data
        return rep

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['owner'] = request.user
        tags = validated_data.pop('tags')
        page = Page.objects.create(**validated_data)
        page.tags.set(tags)

        return page
