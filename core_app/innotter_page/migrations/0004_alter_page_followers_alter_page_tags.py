# Generated by Django 4.0.5 on 2022-06-25 12:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("innotter_page", "0003_alter_page_followers_alter_page_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="page",
            name="followers",
            field=models.ManyToManyField(
                blank=True, related_name="follows", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="page",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="pages", to="innotter_page.tag"
            ),
        ),
    ]
