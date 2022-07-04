from rest_framework.routers import DefaultRouter
from django.urls import path

from innotter_post.views import PostViewSet

router = DefaultRouter()


app_name = 'posts'

urlpatterns = [
    path('posts/<int:pk>/', PostViewSet.as_view({'get': 'retrieve',
                                                 'post': 'create'})),
    path('posts/page/<int:pk>', PostViewSet.as_view({'get': 'list'})),
    path('posts/', PostViewSet.as_view({'get': 'list'})),
]
