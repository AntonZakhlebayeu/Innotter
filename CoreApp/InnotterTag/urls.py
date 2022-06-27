from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from InnotterTag.views import (
    TagList, AllTagList
)

app_name = 'Tags'
urlpatterns = [
    path('page/<int:pk>/tags/', TagList.as_view()),
    path('page/<int:pk>/tag/<int:pk_tag>/', TagList.as_view()),
    path('tags/', AllTagList.as_view()),
    path('tags/<int:pk>/', AllTagList.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
