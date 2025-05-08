from fastapi import FastAPI
from .routers import categories, users, transactions, auth
import os
from app.routers import celery_router, task_router, pdf_report, notify

app = FastAPI()

print("✅ DATABASE_URL = ", os.getenv("DATABASE_URL"))

app.include_router(notify.router)
app.include_router(pdf_report.router)
app.include_router(task_router.router)
app.include_router(celery_router.router)
app.include_router(categories.router)
app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(auth.router)