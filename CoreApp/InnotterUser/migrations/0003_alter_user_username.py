# Generated by Django 4.0.5 on 2022-06-23 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InnotterUser', '0002_alter_user_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(db_index=True, max_length=255, unique=True),
        ),
    ]
