import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.settings import settings


def send_email(to_email: str, subject: str, message: str) -> bool:
    msg = MIMEMultipart()
    msg['From'] = settings.EMAIL_FROM
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    try:
        with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.send_message(msg)

            print(f'Письмо отправлено на {to_email}')
            return True

    except Exception as e:
        print(f'Ошибка при отправке письма: {e}')
        return False