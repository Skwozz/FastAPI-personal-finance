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

async def update_transactions(session: AsyncSession,transactions_id:int, user_id:int, transactions_update):
    result = await session.execute(
        select(models.Transaction).where(
            models.Transaction.id == transactions_id,
            models.Transaction.user_id == user_id,
        )
    )
    transaction = result.scalars().first()
    transaction.amount = transactions_update.amount
    transaction.description = transactions_update.description
    transaction.date = transactions_update.date
    transaction.category_id = transactions_update.category_id

    await session.commit()
    await session.refresh(transaction)
    return transaction


async def delete_transactions(session: AsyncSession,transactions_id:int, user_id:int):
    result = await session.execute(
        select(models.Transaction).where(
            models.Transaction.id == transactions_id,
            models.Transaction.user_id == user_id,
        )
    )
    transaction = result.scalars().first()
    if not transaction:
        return False

    await session.delete(transaction)
    await session.commit()
    return transaction

