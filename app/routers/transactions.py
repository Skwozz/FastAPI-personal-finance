from fastapi import APIRouter, Depends, HTTPException,Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app import schemas_transaction, crud_transaction
from app.routers.auth import get_current_user
from app.models import User
from app import models
from enum import Enum
from  typing import List




router = APIRouter()

@router.post("/transactions/", response_model=schemas_transaction.TransactionRead)
async def create_transaction(
    transaction: schemas_transaction.TransactionCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await crud_transaction.create_transactions(session, transaction, user_id=current_user.id)

class SortOrder(str,Enum):
    asc = 'asc'
    desc = 'desc'


@router.get("/transactions/", response_model=list[schemas_transaction.TransactionRead])
async def read_transactions(
    sort_by: str = Query('date', enum=['date','amount']),
    order: SortOrder = Query('desc'),
    category_type: models.CategoryType | None = None,
    amount_from: float | None = None,
    amount_to: float | None = None,
    search: str | None = None,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    stmt = select(models.Transaction).where(models.Transaction.user_id==current_user.id,
                                            models.Transaction.is_deleted==False)
    if category_type:
        stmt = stmt.join(models.Category).where(models.Category.type==category_type)

    if amount_from is not None:
        stmt = stmt.where(models.Transaction.amount >= amount_from)
    if amount_to is not None:
        stmt = stmt.where(models.Transaction.amount <= amount_to)
    if search:
        stmt = stmt.where(models.Transaction.description.ilike(f"%{search}%"))

    sort_column = models.Transaction.date if sort_by == 'date' else models.Transaction.amount


    if order == SortOrder.desc:
        stmt = stmt.order_by(sort_column.desc())
    else:
        stmt = stmt.order_by(sort_column.asc())

    result = await session.execute(stmt)

    return result.scalars().all()

@router.put("/transactions/{transactions_id}", response_model= schemas_transaction.TransactionUpdate)
async def update_transactions(
        transaction_id: int,

        transaction_update: schemas_transaction.TransactionUpdate,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user),

):
    transaction = await crud_transaction.update_transactions(session, transaction_id,
                                                             current_user.id,
                                                             transaction_update)
    if not transaction:
        raise HTTPException(status_code=404, detail='Транзакция не найдена')

    return transaction

@router.delete("/transactions/{transaction_id}", status_code= status.HTTP_204_NO_CONTENT )
async def delete_transactions(
        transaction_id: int,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user),

):
    transaction = await crud_transaction.delete_transactions(session, transaction_id,current_user.id)
    if not transaction:
        raise HTTPException(status_code=404, detail='Транзакция не найдена')

    return transaction