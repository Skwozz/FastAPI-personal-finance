from datetime import datetime
from app.celery import celery_app



@celery_app.task
def write_to_file(content: str):
    with open("output.txt", "a") as f:
        f.write(f"[{datetime.now()}] {content}\n")