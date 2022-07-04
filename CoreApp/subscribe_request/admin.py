from django.contrib import admin

from subscribe_request.models import SubscribeRequest


class SubscribeRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'initiator_user',
        'desired_page',
        'is_accepted',
    )


admin.site.register(SubscribeRequest, SubscribeRequestAdmin)
