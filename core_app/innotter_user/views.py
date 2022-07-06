from datetime import datetime

from django.views.generic import detail
from innotter_user.mixins import UserMixin
from innotter_user.models import User
from innotter_user.permissions import IsInRoleAdmin
from innotter_user.renderers import UserJSONRenderer
from innotter_user.serializers import (
    LoginSerializer,
    RegistrationSerializer,
    UserAdministrateSerializer,
    UserSerializer,
)
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.generics import RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class UserViewSet(UserMixin):
    queryset = User.objects.all()
