from fastapi import FastAPI
from .routers import categories, users, transactions, auth
import os
app = FastAPI()

print("✅ DATABASE_URL = ", os.getenv("DATABASE_URL"))

app.include_router(categories.router)
app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(auth.router)