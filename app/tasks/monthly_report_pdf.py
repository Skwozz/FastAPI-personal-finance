from app.celery_config import celery_app
from reportlab.pdfgen import canvas
import os

@celery_app.task
def generate_pdf_report(username: str) -> str:
    output_path = f'generate_reports/{username}.pdf'
    os.makedirs('generate_reports',exist_ok=True)
    c = canvas.Canvas(output_path)
    c.drawString(100,750, f'Отчет для пользователя {username}')
    c.drawString(100,750, 'Спасибо за использование нашего сервиса!')
    c.save()
    return  output_path