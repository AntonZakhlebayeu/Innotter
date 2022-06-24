from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, UsersAllAPIView, UserDetailApiView
)

app_name = 'InnoterUser'
urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('users/<int:pk>/', UserDetailApiView.as_view()),
    path('users/all/', UsersAllAPIView.as_view())
]
