from rest_framework.routers import DefaultRouter

from subscribe_request.views import SubscribeRequestViewSet

router = DefaultRouter()

app_name = 'subscribe_requests'

router.register(r'subscribe_requests', SubscribeRequestViewSet, basename='subscribe_requests')
urlpatterns = router.urls
