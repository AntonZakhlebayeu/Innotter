from rest_framework import serializers
from .models import Page


class PageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.pk')

    class Meta:
        model = Page
        fields = ['uuid', 'title', 'description', 'tags', 'owner', 'followers', 'is_private']
