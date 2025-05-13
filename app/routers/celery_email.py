from fastapi import APIRouter, Depends
from .auth import get_current_user
from app.models import User
from app.tasks import send_email_task

router = APIRouter(prefix="/celery", tags=["celery"])

@router.post("/send-email")
def send_test_email(
    current_user: User = Depends(get_current_user)
):
    task = send_email_task.delay(
        to_email=current_user.email,
        subject="Привет от FastAPI!",
        message="Это письмо отправлено через Celery + Redis"
    )
    return {"task_id": task.id}