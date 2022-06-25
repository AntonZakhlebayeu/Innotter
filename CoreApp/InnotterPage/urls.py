from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    PageDetail, PageList
)

app_name = 'Pages'
urlpatterns = [
    path('page/<int:pk>/', PageDetail.as_view()),
    path('pages/', PageList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)