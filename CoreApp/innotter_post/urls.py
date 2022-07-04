from rest_framework.routers import DefaultRouter
from django.urls import path

from innotter_post.views import PostViewSet

router = DefaultRouter()


app_name = 'posts'

urlpatterns = [
    path('posts/page/<int:pk_page>/', PostViewSet.as_view({'get': 'list',
                                                           'post': 'create'})),
    path('posts/page/<int:pk_page>/post/<int:pk>/', PostViewSet.as_view({'get': 'retrieve',
                                                                         'put': 'update',
                                                                         'delete': 'destroy'})),
    path('posts/get_all_posts/', PostViewSet.as_view({'get': 'get_all_posts'}))
]
