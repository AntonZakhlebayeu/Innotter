from rest_framework import serializers

from InnotterPage.models import Page
from innotter_post.models import Post


class CreatePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['content', 'reply_to', 'created_at', 'updated_at']

    def create(self, validated_data):
        kwargs = self.context.get('request').parser_context['kwargs']
        validated_data['page'] = Page.objects.get(pk=kwargs['pk'])

        post = Post.objects.create(**validated_data)

        return post


class UpdatePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['content']


class RetrievePostSerializer(serializers.ModelSerializer):
    page = serializers.ReadOnlyField(source='page.uuid')

    class Meta:
        model = Post
        fields = ['page', 'content', 'reply_to', 'created_at', 'updated_at', 'replies']


class ListPostSerializer(serializers.ModelSerializer):
    page = serializers.ReadOnlyField(source='page.uuid')

    class Meta:
        model = Post
        fields = ['page', 'content', 'reply_to', 'created_at', 'updated_at', 'replies']

