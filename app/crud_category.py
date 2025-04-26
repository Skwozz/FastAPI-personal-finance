from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas_category


async def get_categories(session: AsyncSession, user_id:int):
    result = await session.execute(select(models.Category).where(models.Category.user_id==user_id))
    return result.scalars().all()

async def create_category(session: AsyncSession, category: schemas_category.CategoryCreate, user_id:int):
    db_category = models.Category(
        name=category.name,
        type=category.type,
        user_id=user_id,
    )
    session.add(db_category)
    await session.commit()
    await session.refresh(db_category)
    return db_category
