from rest_framework import serializers

from InnotterPage.models import Page
from InnotterTag.models import Tag


class TagSerializer(serializers.ModelSerializer):
    pages = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'pages']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['pages'] = ForTagPageSerializer(instance.pages.all(), many=True).data
        return rep


class TagPageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['name']


class ForTagPageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = ['uuid', 'name', 'owner']
