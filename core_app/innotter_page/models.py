from datetime import datetime

from django.db import models
from pytz import UTC


class Page(models.Model):
    name = models.CharField(max_length=80)
    uuid = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField("innotter_tag.Tag", related_name="pages", blank=True)
    owner = models.ForeignKey(
        "innotter_user.User", on_delete=models.CASCADE, related_name="pages"
    )
    followers = models.ManyToManyField(
        "innotter_user.User", related_name="follows", blank=True
    )
    image = models.URLField(null=True, blank=True)
    is_private = models.BooleanField(default=False)
    unblock_date = models.DateTimeField(null=True, blank=True)
    is_permanent_blocked = models.BooleanField(default=False)

    def is_temporary_blocked(self):
        if self.unblock_date is None:
            return True

        utc_now = datetime.utcnow().replace(tzinfo=UTC)
        utc_unblock_date = self.unblock_date.replace(tzinfo=UTC)
        return utc_now > utc_unblock_date
