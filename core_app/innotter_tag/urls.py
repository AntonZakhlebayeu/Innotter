from django.urls import path
from innotter_tag.views import TagList
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "Tags"
urlpatterns = [
    path(
        "page/<int:pk>/tag/<int:pk_tag>/",
        TagList.as_view({"get": "retrieve", "delete": "destroy"}),
    ),
    path("page/<int:pk>/tags/", TagList.as_view({"get": "list", "post": "create"})),
    path("tag/get_tag/<int:pk>/", TagList.as_view({"get": "get_tag"})),
    path("tags/all/", TagList.as_view({"get": "all"})),
    path("tag/delete_tag/<int:pk>/", TagList.as_view({"delete": "delete_tag"})),
]

urlpatterns = format_suffix_patterns(urlpatterns)
