# Generated by Django 4.0.5 on 2022-07-05 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("innotter_page", "0007_delete_post"),
    ]

    operations = [
        migrations.AddField(
            model_name="page",
            name="is_permanent_blocked",
            field=models.BooleanField(default=False),
        ),
    ]
