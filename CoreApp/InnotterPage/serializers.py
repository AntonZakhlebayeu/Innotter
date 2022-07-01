from rest_framework import serializers

import InnotterUser.serializers
from InnotterTag.models import Tag
from InnotterTag.serializers import TagPageSerializer, TagSerializer
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

    def create(self, validated_data):

        tags = []

        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        for tag in validated_data.pop('tags', ):
            try:
                Tag.objects.get(name=tag['name']).pk
            except Tag.DoesNotExist:
                tag_serializer = TagSerializer(data={"name": tag['name']})
                tag_serializer.is_valid()
                tag_serializer.save()

            tags.append(Tag.objects.get(name=tag['name']).pk)

        validated_data['owner'] = user

        page = Page.objects.create(**validated_data)
        page.tags.set(tags)

        return page

    def update(self, instance, validated_data, *args, **kwargs):

        for key, value in validated_data.items():
            if key == 'tags':
                tag_id = []

                for tag_dict in value:

                    try:
                        Tag.objects.get(name=tag_dict['name'])
                    except Tag.DoesNotExist:

                        tag_serializer = TagSerializer(data={"name": tag_dict['name']})
                        tag_serializer.is_valid()
                        tag_serializer.save()

                    tag_id.append(Tag.objects.get(name=tag_dict['name']).pk)

                instance.tags.set(tag_id)

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
