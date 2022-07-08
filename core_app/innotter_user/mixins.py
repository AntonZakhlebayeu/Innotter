from datetime import datetime

from innotter_user.models import User
from innotter_user.permissions import IsInRoleAdmin
from innotter_user.serializers import (
    LoginSerializer,
    RegistrationSerializer,
    UserSerializer,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import (
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core_app.default_mixin import GetPermissionsMixin, GetSerializerMixin


class UserMixin(
    GetSerializerMixin,
    GetPermissionsMixin,
    viewsets.GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    serializer_classes = {
        "update": UserSerializer,
        "partial_update": UserSerializer,
        "retrieve": UserSerializer,
        "list": UserSerializer,
        "register": RegistrationSerializer,
        "login": LoginSerializer,
        "update_me": UserSerializer,
        "me": UserSerializer,
        "block": UserSerializer,
        "unblock": UserSerializer,
    }

    permission_classes = {
        "update": (
            IsAuthenticated,
            IsInRoleAdmin,
        ),
        "partial_update": (
            IsAuthenticated,
            IsInRoleAdmin,
        ),
        "retrieve": (
            IsAuthenticated,
            IsInRoleAdmin,
        ),
        "list": (
            IsAuthenticated,
            IsInRoleAdmin,
        ),
        "destroy": (
            IsAuthenticated,
            IsInRoleAdmin,
        ),
        "register": (AllowAny,),
        "login": (AllowAny,),
        "me": (IsAuthenticated,),
        "update_me": (IsAuthenticated,),
        "block": (
            IsAuthenticated,
            IsInRoleAdmin,
        ),
        "unblock": (
            IsAuthenticated,
            IsInRoleAdmin,
        ),
    }

    def retrieve(self, request, *args, **kwargs):
        if User.objects.filter(pk=kwargs["pk"]).first() is None:
            return Response(
                {"detail": "Not Found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(User.objects.get(pk=kwargs["pk"]))

        access_token = request.COOKIES["access_token"]
        response_dict = {"access_token": access_token}
        response_dict.update(serializer.data)
        response = Response(response_dict, status=status.HTTP_200_OK)
        response.set_cookie("access_token", access_token)

        return response

    def update(self, request, *args, **kwargs):
        if User.objects.filter(pk=kwargs["pk"]).first() is None:
            return Response(
                {"detail": "Not Found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer_data = request.data.get(
            "user",
        )

        serializer = self.get_serializer(
            User.objects.get(pk=kwargs.get("pk")),
            data=serializer_data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=("post",),
        permission_classes=(
            {
                "login": (AllowAny,),
            }
        ),
    )
    def login(self, request):
        user = request.data.get(
            "user",
        )
        user_model = User.objects.get(email=user["email"])

        if user_model.is_blocked:
            return Response(
                {"detail": "You are blocked."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_model.last_login = datetime.now()
        user_model.save()

        serializer = self.get_serializer(data=user)
        serializer.is_valid(raise_exception=True)

        response = Response(serializer.data, status=status.HTTP_200_OK)

        response.set_cookie(
            "access_token",
            serializer.data.get(
                "access_token",
            ),
            httponly=True,
        )
        response.set_cookie(
            "refresh_token",
            serializer.data.get(
                "refresh_token",
            ),
            httponly=True,
        )

        return response

    @action(
        detail=False,
        methods=("post",),
        permission_classes=(
            {
                "register": (AllowAny,),
            }
        ),
    )
    def register(self, request):
        user = request.data.get(
            "user",
        )

        serializer = self.get_serializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=("get",),
        permission_classes=(
            {
                "me": (IsAuthenticated,),
            }
        ),
    )
    def me(self, request):
        return Response(
            self.get_serializer(request.user).data, status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        methods=("put",),
        permission_classes=(
            {
                "update_me": (IsAuthenticated,),
            }
        ),
    )
    def update_me(self, request):
        serializer_data = request.data.get(
            "user",
        )

        serializer = self.get_serializer(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=("put",),
        permission_classes=(
            {
                "block": (
                    IsAuthenticated,
                    IsInRoleAdmin,
                ),
            }
        ),
    )
    def block(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs.get("pk", None))

        user.is_blocked = True
        user.save()

        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=("put",),
        permission_classes=(
            {
                "unblock": (
                    IsAuthenticated,
                    IsInRoleAdmin,
                ),
            }
        ),
    )
    def unblock(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs.get("pk", None))

        user.is_blocked = False
        user.save()

        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
