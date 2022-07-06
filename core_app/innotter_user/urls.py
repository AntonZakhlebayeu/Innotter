from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    LoginAPIView,
    RegistrationAPIView,
    UsersAPIView,
    UserUpdateAPIView,
)

app_name = "InnoterUser"
urlpatterns = [
    path("users/", RegistrationAPIView.as_view()),
    path("users/login/", LoginAPIView.as_view()),
    path(
        "users/<int:pk>/",
        UsersAPIView.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
    path("users/all/", UsersAPIView.as_view({"get": "list"})),
    path("users/<int:pk>/block/", UsersAPIView.as_view({"put": "update"})),
    path("users/me/", UserUpdateAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
