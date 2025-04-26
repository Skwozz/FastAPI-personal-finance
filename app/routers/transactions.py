from fastapi import APIRouter, Depends
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
