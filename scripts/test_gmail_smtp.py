from app.services.email_service import send_email

if __name__ == "__main__":
    result = send_email(
        to_email="osu.master.2000@gmail.com",
        subject="Проверка Gmail SMTP",
        message="Если ты видишь это письмо — значит SMTP с Gmail работает!"
    )
    print("Успешно" if result else "Ошибка")
