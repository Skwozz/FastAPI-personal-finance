import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.settings import settings
from app.celery import celery_app



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