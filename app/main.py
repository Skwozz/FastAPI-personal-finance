from fastapi import FastAPI
from .routers import categories, users, transactions, auth

app = FastAPI()

@app.get('/')
async def root():
    return {'message':'alive!'}

app.include_router(categories.router)
app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(auth.router)