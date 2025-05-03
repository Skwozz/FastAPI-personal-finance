# Используем официальный образ Python
FROM python:3.11



# Установка системных зависимостей
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Создаём рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё приложение
COPY . .

COPY wait-for-it.sh .
RUN chmod +x wait-for-it.sh
# Команда по умолчанию
CMD ["./wait-for-it.sh", "db:5432", "--", "bash", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]