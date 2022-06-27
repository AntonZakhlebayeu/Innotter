from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    PageList, PageBlocking, PageUnblocking
)

app_name = 'Pages'
urlpatterns = [
    path('pages/', PageList.as_view()),
    path('pages/<int:pk>/', PageList.as_view()),
    path('pages/block/', PageBlocking.as_view()),
    path('pages/unblock/', PageUnblocking.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
