import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core_app.settings")

app = Celery("core_app")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task
def error_handler(request, exc, traceback):
    print("Task {0} raised exception: {1!r}\n{2!r}".format(request.id, exc, traceback))
