from django.contrib.auth import authenticate
from rest_framework import serializers

from InnotterUser.models import User
from InnotterPage.serializers import SmallPageInfoSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'title', 'role', 'password', 'access_token', 'refresh_token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', )
        password = data.get('password', )

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'email': user.email,
            'username': user.username,
            'access_token': user.access_token,
            'refresh_token': user.set_and_get_refresh_token,
        }


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    pages = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    follows = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'is_active', 'is_staff', 'role', 'pages', 'refresh_token', 'follows', 'is_blocked']
        read_only_fields = ['is_active', 'is_staff', 'role', 'pages', 'follows']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["pages"] = SmallPageInfoSerializer(instance.pages.all(), many=True).data
        rep['follows'] = SmallPageInfoSerializer(instance.pages.all(), many=True).data
        return rep

    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class UsernameSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']
        read_only_fields = ['username']

