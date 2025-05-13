import os
import smtplib
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from reportlab.pdfgen import canvas

from app.settings import settings
from .celery import celery_app
from .utils.email_generator import send_email


@celery_app.task
def test_add(x: int, y: int) -> int:
    return x + y

@celery_app.task
def write_to_file(content: str):
    with open("output.txt", "a") as f:
        f.write(f"[{datetime.now()}] {content}\n")

@celery_app.task
def generate_pdf_report(username: str) -> str:
    output_path = f'generate_reports/{username}.pdf'
    os.makedirs('generate_reports',exist_ok=True)
    c = canvas.Canvas(output_path)
    # c.drawString(100,750, f'Отчет для пользователя {username}')
    # c.drawString(100,750, 'Спасибо за использование нашего сервиса!')
    c.save()
    return  output_path


@celery_app.task
def send_email_task(to_email: str, subject: str, message: str):
    return send_email(to_email,subject,message)

@celery_app.task
def send_financial_report_email(to_email: str, transactions: list[dict]):
    from app.utils.pdf_generator import generate_pdf

    msg = MIMEMultipart()
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = to_email
    msg["Subject"] = "Ваш финансовый отчёт"

    msg.attach(MIMEText("Привет! Вложение — PDF со списком твоих транзакций.", "plain"))

    try:
        pdf_buffer = generate_pdf(transactions)
        part = MIMEApplication(pdf_buffer.read(), Name="report.pdf")
        part["Content-Disposition"] = 'attachment; filename=\"report.pdf\"'
        msg.attach(part)

        with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.send_message(msg)

        print(f"Отчёт отправлен на {to_email}")
        return True

    except Exception as e:
        print(f"Ошибка при отправке отчёта: {e}")
        return False
