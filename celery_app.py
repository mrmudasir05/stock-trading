from celery import Celery

redis_url = "redis://localhost:6379/0"
celery_app = Celery(
    "stocktrading",
    broker=redis_url,
    backend=redis_url,
    include=["utils.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True
)