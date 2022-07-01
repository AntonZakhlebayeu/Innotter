from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

from InnotterPage.views import (
    PageList, PageBlocking, PageUnblocking
)

router = routers.SimpleRouter()
router.register(r'pages', PageList)

app_name = 'Pages'
urlpatterns = [
    path('', include(router.urls)),
    path('pages/block/', PageBlocking.as_view()),
    path('pages/unblock/', PageUnblocking.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
