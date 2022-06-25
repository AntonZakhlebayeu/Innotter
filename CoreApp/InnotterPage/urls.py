from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    PageDetail, PageList, TagList, TagDetail, AllTagList, TagsAdministrate
)

app_name = 'Pages'
urlpatterns = [
    path('page/<int:pk>/', PageDetail.as_view()),
    path('pages/', PageList.as_view()),
    path('page/<int:pk>/tags/', TagList.as_view()),
    path('page/<int:pk>/tag/<int:pk_tag>/', TagDetail.as_view()),
    path('tags/', AllTagList.as_view()),
    path('tags/<int:pk>/', TagsAdministrate.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)