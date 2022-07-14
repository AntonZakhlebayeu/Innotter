from django.urls import include, path
from innotter_page.views import PageList
from innotter_post.views import AllPostViewSet, PostViewSet
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

router = SimpleRouter()
router.register("pages", PageList)

post_router = routers.NestedSimpleRouter(router, r"pages", lookup="pages")

post_router.register(r"posts", PostViewSet, basename="page")

app_name = "posts"

urlpatterns = [
    path("", include(post_router.urls)),
    path("posts/", AllPostViewSet.as_view({"get": "get_all_posts"})),
]
