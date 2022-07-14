from innotter_user.mixins import UserMixin
from innotter_user.models import User


class UserViewSet(UserMixin):
    queryset = User.objects.all()
