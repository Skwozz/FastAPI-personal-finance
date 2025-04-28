import asyncio

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud_user, schemas_user, models
from app.database import get_session
from app.routers.auth import get_current_user

router = APIRouter()

@router.post("/users/", response_model=schemas_user.UserRead)
async def register_user(user: schemas_user.UserCreate, session: AsyncSession = Depends(get_session)):
    existing = await crud_user.get_user_by_username(session, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")
    return await crud_user.create_user(session, user)


@router.get("/me", response_model=schemas_user.UserMe)
async def read_users_me(
        current_user: models.User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)):
    categories_count, transactions_count = await asyncio.gather(
        session.scalar(select(func.count(models.Category.id)).where(models.Category.user_id == current_user.id)),

        session.scalar(select(func.count(models.Transaction.id)).where(models.Transaction.user_id == current_user.id)))

    income_sum, expense_sum = await asyncio.gather(
        session.scalar
        (select(func.coalesce(func.sum(models.Transaction.amount), 0)).
         join(models.Category)
         .where(models.Transaction.user_id == current_user.id,
                models.Category.type == 'INCOME')),
        session.scalar
        (select(func.coalesce(func.sum(models.Transaction.amount), 0))
        .join(models.Category)
        .where(models.Transaction.user_id == current_user.id,
               models.Category.type == 'EXPENSE')))

    return schemas_user.UserMe(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        categories_count=categories_count,
        transactions_count=transactions_count,
        income_total=income_sum,
        expense_total=expense_sum
    )
