from django.db import models


class Like(models.Model):
    post = models.ForeignKey(
        'innotter_post.Post',
        on_delete=models.SET_NULL,
        related_name='likes',
        blank=True,
        null=True
    )
    owner = models.ForeignKey(
        'InnotterUser.User',
        on_delete=models.SET_NULL,
        related_name='likes',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'like_{self.id}'
