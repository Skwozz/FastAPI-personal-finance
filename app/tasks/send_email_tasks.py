from app.celery_config import celery_app
from app.services.email_service import send_email

@celery_app.task
def send_email_task(to_email: str, subject: str, message: str):
    return send_email(to_email,subject,message)