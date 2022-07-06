from django.urls import include, path
from innotter_page.views import PageList
from innotter_tag.views import TagList
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

router = SimpleRouter()
router.register("pages", PageList)

tags_router = routers.NestedSimpleRouter(router, r"pages", lookup="pages")

tags_router.register(r"tags", TagList, basename="page")

app_name = "tags"

urlpatterns = [
    path("", include(tags_router.urls)),
]
