from celery import Celery
# from app.tasks import add
celery_app = Celery(
    'worker',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

print("✅ Celery инициализирован и ждёт задачи...")
celery_app.autodiscover_tasks(["app.tasks"])
