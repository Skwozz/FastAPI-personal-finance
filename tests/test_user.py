import pytest
# @pytest.fixture(scope='session', autouse=True)
@pytest.mark.asyncio
async def test_register_login_and_me(client):
    # Регистрация пользователя
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    response = await client.post("/users/", json=user_data)
    print("REGISTER:", response.status_code, response.text)
    assert response.status_code in (200, 400)
    # Получение токена
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = await client.post("/auth/token", data=login_data)
    print("TOKEN:", response.status_code, response.text)
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Запрос /me
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/me", headers=headers)

    # Проверка содержимого
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"
    assert "categories_count" in data
    assert "transactions_count" in data
