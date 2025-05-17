import os
from reportlab.pdfgen import canvas
from app.celery import celery_app



@celery_app.task
def generate_pdf_report(username: str) -> str:
    output_path = f'generate_reports/{username}.pdf'
    os.makedirs('generate_reports',exist_ok=True)
    c = canvas.Canvas(output_path)
    c.save()
    return  output_path
