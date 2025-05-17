#  Personal Finance API

Асинхронное backend-приложение для учёта личных финансов с возможностью:
- хранения транзакций (доходы / расходы),
- генерации PDF-отчётов,
- отправки писем с вложениями через Celery + Redis,
- работы внутри Docker-окружения.

---

## Функционал

-  JWT-аутентификация пользователей
-  CRUD-операции над транзакциями и категориями
-  Сортировка, фильтрация, soft delete
-  Отправка писем через SMTP (Mail.ru)
-  Генерация PDF с отчётом по транзакциям
-  Фоновая обработка задач с Celery
-  Docker + docker-compose
-  Alembic миграции
-  Тесты через `pytest`, `httpx`, `asyncio`

---

## Стек

- **FastAPI — асинхронный веб-фреймворк
- PostgreSQL — база данных
- SQLAlchemy 2.0 — ORM (async)
- Alembic — миграции
- Pydantic — валидация и схемы
- Celery + Redis — фоновые задачи
- ReportLab — генерация PDF
- Docker — изоляция окружения
- Pytest + HTTPX — тестирование

---

##  Запуск проекта через Docker

```bash
git clone https://github.com/Skwozz/FastAPI-personal-finance.git
cd FastAPI-personal-finance
cp .env.example .env  # создай и заполни .env
docker-compose up --build
```
##Структура проекта

app/
├── crud/             # SQL-операции
├── schemas/          # Pydantic-модели
├── routers/          # Эндпоинты
├── tasks/            # Celery-задачи
├── services/         # Бизнес-логика
├── core/             # PDF, конфиги
├── models.py         # SQLAlchemy-модели
├── main.py           # Точка входа

Автор: Skwozz(Нифантов Семен Алексеевич) 
Разработано в рамках подготовки к трудоустройству
