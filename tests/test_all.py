import pytest
from httpx import AsyncClient, ASGITransport
from app.database import Base, test_engine
from tests.test_app import create_test_app

@pytest.mark.asyncio
async def test_full_flow():
    # Полностью чистим тестовую БД
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Создаём приложение с тестовой сессией
    app = create_test_app()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Регистрируем пользователя
        user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword"
        }
        response = await client.post("/users/", json=user_data)
        assert response.status_code in (200, 400)

        # Получаем токен
        response = await client.post("/auth/token", data={
            "username": "testuser",
            "password": "testpassword"
        })
        assert response.status_code == 200
        token = response.json()["access_token"]
        client.headers.update({"Authorization": f"Bearer {token}"})

        # Проверка /me
        response = await client.get("/me")
        assert response.status_code == 200
        assert response.json()["username"] == "testuser"

        # Создаём категорию
        category_data = {"name": "Еда", "type": "EXPENSE"}
        response = await client.post("/categories/", json=category_data)
        assert response.status_code == 200
        category_id = response.json()["id"]

        # Создаём транзакцию
        transaction_data = {
            "amount": 500.0,
            "description": "Пельмени",
            "date": "2025-04-30T00:00:00",
            "category_id": category_id
        }
        response = await client.post("/transactions/", json=transaction_data)
        assert response.status_code == 200
        transaction_id = response.json()["id"]

        # Проверка: транзакция есть
        response = await client.get("/transactions/")
        assert any(t["id"] == transaction_id for t in response.json())

        # Удаляем (soft delete)
        response = await client.delete(f"/transactions/{transaction_id}")
        assert response.status_code in (200, 204)

        # Проверка: транзакции больше нет
        response = await client.get("/transactions/")
        assert all(t["id"] != transaction_id for t in response.json())
