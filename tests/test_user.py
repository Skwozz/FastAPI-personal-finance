# import pytest
#
# @pytest.mark.asyncio
# async def test_register_login_and_me(authorized_client):
#     # Тест эндпоинта /me
#     response = await authorized_client.get("/me")
#     assert response.status_code == 200
#     data = response.json()
#
#     assert data["username"] == "testuser"
#     assert data["email"] == "testuser@example.com"
#     assert "categories_count" in data
#     assert "transactions_count" in data
