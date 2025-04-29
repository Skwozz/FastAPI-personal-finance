from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_session
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost/fastapi_finance"
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost/test_fastapi_finance"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
test_session = sessionmaker(test_engine,class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_test_session() -> AsyncSession:
    async with async_session() as session:
        yield session