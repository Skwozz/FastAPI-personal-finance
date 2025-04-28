from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app import schemas_transaction, crud_transaction
from app.routers.auth import get_current_user
from app.models import User


router = APIRouter()

@router.post("/transactions/", response_model=schemas_transaction.TransactionRead)
async def create_transaction(
    transaction: schemas_transaction.TransactionCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await crud_transaction.create_transactions(session, transaction, user_id=current_user.id)

@router.get("/transactions/", response_model=list[schemas_transaction.TransactionRead])
async def read_transactions(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):

    return await crud_transaction.get_transactions(session, user_id=current_user.id)

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

@router.delete("/transactions/{transactions_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_transactions(
        transaction_id: int,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user),

):
    transaction = await crud_transaction.delete_transactions(session, transaction_id,current_user.id)
    if not transaction:
        raise HTTPException(status_code=404, detail='Транзакция не найдена')

    return transaction