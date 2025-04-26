from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models,schemas_transaction


async def create_transactions(session: AsyncSession,  transaction: schemas_transaction.TransactionCreate,user_id:int):
    db_transaction = models.Transaction(
        amount=transaction.amount,
        date=transaction.date,
        description=transaction.description,
        category_id=transaction.category_id,
        user_id=user_id,
    )
    session.add(db_transaction)
    await session.commit()
    await session.refresh(db_transaction)
    return db_transaction
async def get_transactions(session: AsyncSession, user_id:int):
    result = await session.execute(select(models.Transaction).where(models.Transaction.user_id==user_id))
    return result.scalars().all()

