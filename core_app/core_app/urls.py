from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("innotter_user.urls", namespace="authentication")),
    path("api/", include("innotter_page.urls", namespace="pages")),
    path("api/", include("innotter_tag.urls", namespace="tags")),
    path("api/", include("subscribe_request.urls", namespace="subscribe_requests")),
    path("api/", include("innotter_post.urls", namespace="posts")),
    path("api/", include("innotter_like.urls", namespace="likes")),
]
