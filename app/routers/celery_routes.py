from fastapi import APIRouter
from app.tasks import test_add, write_to_file
from app.celery import celery_app


router = APIRouter(prefix="/celery", tags=["celery"])

@router.get("/run-task")
async def run_task(x: int = 1, y: int = 2):
    task = test_add.delay(x, y)
    return {"task_id": task.id}

@router.get("/result/{task_id}")
async def get_task_result(task_id: str):
    result = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    }

@router.get("/write/")
async def write(content: str):
    task = write_to_file.delay(content)
    return {"status": "task sent", "task_id": task.id}
