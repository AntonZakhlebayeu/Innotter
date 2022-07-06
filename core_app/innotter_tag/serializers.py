from innotter_page.models import Page
from innotter_tag.models import Tag
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    pages = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ["id", "name", "pages"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["pages"] = ForTagPageSerializer(instance.pages.all(), many=True).data
        return rep

    def create(self, validated_data):
        print(validated_data)
        tag = Tag.objects.create(name=validated_data["name"])

        request = self.context.get("request")
        if request:
            page = Page.objects.get(pk=request.parser_context["kwargs"]["pk"])
            page.tags.add(tag)

        return tag


class TagPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]


class ForTagPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ["uuid", "name", "owner"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        from innotter_user.serializers import UsernameSerializer

        rep["owner"] = UsernameSerializer(instance.owner).data
        return rep
