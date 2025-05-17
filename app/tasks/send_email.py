from app.celery import celery_app
from app.utils.email_generator import send_email


@celery_app.task
def send_email_task(to_email: str, subject: str, message: str):
    return send_email(to_email,subject,message)
