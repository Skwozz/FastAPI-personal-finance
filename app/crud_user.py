from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from app import models, schemas_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_by_username(session: AsyncSession, username: str):
    result = await session.execute(select(models.User).where(models.User.username == username))
    return result.scalars().first()

async def create_user(session: AsyncSession, user: schemas_user.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user