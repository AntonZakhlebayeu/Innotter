from rest_framework import serializers
from .models import Page


class PageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.pk')

    class Meta:
        model = Page
        fields = ['uuid', 'description', 'tags', 'owner', 'followers', 'is_private']

    def update(self, instance, validated_data):

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
