from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('InnotterUser.urls', namespace='authentication')),
    path('api/', include('InnotterPage.urls', namespace='pages')),
    path('api/', include('InnotterTag.urls', namespace='tags')),
    path('api/', include('subscribe_request.urls', namespace='subscribe_requests')),
    path('api/', include('innotter_post.urls', namespace='posts'))
]
