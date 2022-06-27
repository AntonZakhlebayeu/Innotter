from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.response import Response

from InnotterUser.models import User
from InnotterUser.serializers import UserSerializer


class UserMixin(GenericAPIView,
                ListModelMixin,
                CreateModelMixin,
                RetrieveModelMixin):

    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs['pk']
            return self.retrieve(request, *args, **kwargs)
        except KeyError:
            return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = request.data.get('user', )

        user_model = User.objects.get(email=user['email'])
        user_model.is_blocked = user['is_blocked']
        user_model.save()

        return Response(UserSerializer(user_model).data, status=status.HTTP_200_OK)

