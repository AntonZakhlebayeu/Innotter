from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from InnotterTag.views import (
    TagList, AllTagList
)

router_all_tags = routers.SimpleRouter()
router_all_tags.register(r'tags', AllTagList)

app_name = 'Tags'
urlpatterns = [
    path('page/<int:pk>/tag/<int:pk_tag>/', TagList.as_view({'get': 'retrieve',
                                                             'delete': 'destroy'})),
    path('page/<int:pk>/tags/', TagList.as_view({'get': 'list',
                                                 'post': "create"})),
    path('', include(router_all_tags.urls)),
]

urlpatterns = format_suffix_patterns(urlpatterns)
