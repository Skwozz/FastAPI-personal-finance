from fastapi import APIRouter

from app.celery_config import celery_app


router = APIRouter()

celery_app.conf.task_routes = {
    "app.tasks.*": {"queue": "main-queue"}
}


