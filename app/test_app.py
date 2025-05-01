from fastapi import FastAPI
from app.routers import users, transactions, categories, auth
from app.database import get_test_session, get_session

def create_test_app() -> FastAPI:
    app = FastAPI()


    app.dependency_overrides[get_session] = get_test_session

    app.include_router(users.router)
    app.include_router(transactions.router)
    app.include_router(categories.router)
    app.include_router(auth.router)

    return app

