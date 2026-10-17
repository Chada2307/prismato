from celery import Celery

celery_app = Celery(
    "prismato_worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1",
    include=['core.tasks']
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Warsaw",
    enable_utc=True,
)