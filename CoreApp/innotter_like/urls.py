from rest_framework.routers import DefaultRouter

from innotter_like.views import LikeViewSet

router = DefaultRouter()

app_name = 'likes'
router.register(r'likes', LikeViewSet, basename='likes')
urlpatterns = router.urls