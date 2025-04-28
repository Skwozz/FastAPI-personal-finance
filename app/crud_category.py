from fastapi import HTTPException
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

async def update_category(session: AsyncSession, category_id: int, user_id: int, category_update):
    result = await session.execute(
        select(models.Category).where(
            models.Category.id == category_id,
            models.Category.user_id == user_id
        )
    )
    category = result.scalars().first()
    category.name = category_update.name
    category.type = category_update.type
    await session.commit()
    await session.refresh(category)
    return category

async def delete_category(session: AsyncSession, category_id: int, user_id: int):
    result = await session.execute(
        select(models.Category).where(
            models.Category.id == category_id,
            models.Category.user_id == user_id
        )
    )
    category = result.scalars().first()
    if not category:
        raise HTTPException(status_code=404, detail='Категория не найдена')
    await session.delete(category)
    await session.commit()

    return category