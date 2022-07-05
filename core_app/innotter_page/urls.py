from django.urls import path
from innotter_page.views import PageList
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "Pages"
urlpatterns = [
    path("pages/", PageList.as_view({"get": "list", "post": "create"})),
    path(
        "page/<int:pk>/",
        PageList.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
    ),
    path("page/block/", PageList.as_view({"put": "block"})),
    path("page/unblock/", PageList.as_view({"put": "unblock"})),
]

urlpatterns = format_suffix_patterns(urlpatterns)
