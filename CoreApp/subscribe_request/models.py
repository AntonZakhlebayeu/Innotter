from django.db import models


class SubscribeRequest(models.Model):
    initiator_user = models.ForeignKey(
        'InnotterUser.User',
        on_delete=models.SET_NULL,
        related_name='initiator_requests',
        blank=True,
        null=True
    )
    desired_page = models.ForeignKey(
        'InnotterPage.Page',
        on_delete=models.SET_NULL,
        related_name='desired_requests',
        blank=True,
        null=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'request_{self.id}'
