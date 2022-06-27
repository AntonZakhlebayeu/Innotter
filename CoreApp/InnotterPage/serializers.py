from rest_framework import serializers

import InnotterUser.serializers
from InnotterTag.serializers import TagPageSerializer
from InnotterPage.models import Page


class PageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    tags = serializers.JSONField()

    class Meta:
        model = Page
        fields = ['uuid', 'name', 'description', 'tags', 'owner', 'followers', 'is_private', 'unblock_date']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["followers"] = InnotterUser.serializers.UsernameSerializer(instance.followers.all(), many=True).data
        rep['tags'] = TagPageSerializer(instance.tags.all(), many=True).data
        return rep

    def update(self, instance, validated_data):

        for key, value in validated_data.items():
            if key == 'tags':
                instance.tags.set(value)
            else:
                setattr(instance, key, value)

        instance.save()

        return instance


class SmallPageInfoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Page
        fields = ['uuid', 'name', 'owner', 'is_private', 'tags']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['tags'] = TagPageSerializer(instance.tags.all(), many=True).data
        return rep

