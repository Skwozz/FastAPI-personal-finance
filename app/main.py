from fastapi import FastAPI
from .routers import categories, users, transactions, auth, celery_email_pdf
from app.routers import celery_routes, celery_pdf, celery_email
app = FastAPI()

@app.get('/')
async def root():
    return {'message':'alive!'}


app.include_router(celery_email_pdf.router)
app.include_router(celery_email.router)
app.include_router(celery_pdf.router)
app.include_router(celery_routes.router)
app.include_router(categories.router)
app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(auth.router)