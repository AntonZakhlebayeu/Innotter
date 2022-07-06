from innotter_like.views import LikeViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

app_name = "likes"
router.register(r"likes", LikeViewSet, basename="likes")
urlpatterns = router.urls
