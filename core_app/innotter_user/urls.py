from django.urls import include, path
from innotter_user.views import UserViewSet
from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns

router = SimpleRouter()
router.register("users", UserViewSet)

app_name = "Users"
urlpatterns = [
    path("", include(router.urls)),
]

urlpatterns = format_suffix_patterns(urlpatterns)
