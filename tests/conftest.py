import pytest
from httpx import AsyncClient
from app.main import app
from app.database import Base, test_engine, get_test_session, get_session

# Автоматически создаём таблицы в тестовой БД при запуске тестов
@pytest.fixture(scope='session', autouse=True)
async def setup_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

# Переопределяем зависимость get_session → get_test_session
@pytest.fixture
async def client():
    app.dependency_overrides[get_session] = get_test_session
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
    app.dependency_overrides.clear()
