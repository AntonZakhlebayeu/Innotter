from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, UsersAllAPIView
)

app_name = 'InnoterUser'
urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('users/<int:pk>/', UsersAllAPIView.as_view()),
    path('users/all/', UsersAllAPIView.as_view()),
    path('users/block/', UsersAllAPIView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
