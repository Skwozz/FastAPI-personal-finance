from celery.result import AsyncResult
from fastapi import APIRouter
from app.celery_config import celery_app


router = APIRouter()



@router.get("/status/{task_id}")
def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.successful() else None
    }