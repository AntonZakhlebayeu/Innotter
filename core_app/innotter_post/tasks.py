from time import sleep

from celery import shared_task
from django.core.mail import send_mail

from core_app.settings import EMAIL_HOST_USER


@shared_task
def send_email_to_followers_task(**kwargs):
    if len(kwargs.get("emails")) > 0:
        send_mail(
            f'There is a new post on the {kwargs.get("page_name")} ',
            "Check it out!",
            EMAIL_HOST_USER,
            kwargs.get("emails"),
        )

    return None
