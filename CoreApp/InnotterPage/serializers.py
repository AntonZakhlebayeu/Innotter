from rest_framework import serializers

import InnotterUser.serializers
from .models import Page, Tag


class PageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Page
        fields = ['uuid', 'name', 'description', 'tags', 'owner', 'followers', 'is_private']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["followers"] = InnotterUser.serializers.FollowerSerializer(instance.followers.all(), many=True).data
        rep['tags'] = TagPageSerializer(instance.tags.all(), many=True).data
        return rep

    def update(self, instance, validated_data):

        for key, value in validated_data.items():
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


class TagSerializer(serializers.ModelSerializer):
    pages = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'pages']

    def update(self, instance, validated_data):

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class TagPageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['name']

