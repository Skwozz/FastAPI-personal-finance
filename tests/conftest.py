# import pytest
# from httpx import AsyncClient, ASGITransport
# from app.main import app
# from app.database import Base, test_engine, get_test_session, get_session
#
#
# @pytest.fixture(scope="module", autouse=True)
# async def setup_test_db():
#     async with test_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#
#
# @pytest.fixture
# async def client():
#     app.dependency_overrides[get_session] = get_test_session
#     async with AsyncClient(
#         transport=ASGITransport(app=app),
#         base_url="http://test"
#     ) as ac:
#         yield ac
#     app.dependency_overrides.clear()
#
# @pytest.fixture
# async def authorized_client(client):
#     user_data = {
#         "username": "testuser",
#         "email": "testuser@example.com",
#         "password": "testpassword"
#     }
#     await client.post("/users/", json=user_data)
#
#     login_data = {
#         "username": "testuser",
#         "password": "testpassword"
#     }
#     response = await client.post("/auth/token", data=login_data)
#     assert response.status_code == 200
#     token = response.json()["access_token"]
#
#
#     async with AsyncClient(
#         transport=ASGITransport(app=app),
#         base_url="http://test",
#         headers={"Authorization": f"Bearer {token}"}
#     ) as auth_client:
#         yield auth_client
