from datetime import datetime

from rest_framework import status, generics
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .permissions import IsInRoleAdmin
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = [UserJSONRenderer]

    def post(self, request):
        user = request.data.get('user', )

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', )

        user_model = User.objects.get(email=user['email'])
        user_model.last_login = datetime.now()
        user_model.save()

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        response = Response(serializer.data, status=status.HTTP_200_OK)

        response.set_cookie('access_token', serializer.data.get('access_token', ), httponly=True)
        response.set_cookie('refresh_token', serializer.data.get('refresh_token', ), httponly=True)

        return response


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        access_token = request.COOKIES['access_token']
        response_dict = {
            'access_token': access_token
        }
        response_dict.update(serializer.data)
        response = Response(response_dict, status=status.HTTP_200_OK)
        response.set_cookie('access_token', access_token)

        return response

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', )

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        access_token = request.COOKIES['access_token']
        response_dict = {
            'access_token': access_token
        }
        response_dict.update(serializer.data)
        response = Response(response_dict, status=status.HTTP_200_OK)
        response.set_cookie('access_token', access_token, httponly=True)

        return response


class UsersAllAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsInRoleAdmin,)
    serializer_class = UserSerializer

    queryset = User.objects.all()


class UserDetailAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsInRoleAdmin,)
    serializer_class = UserSerializer
    queryset = User.objects.all()





