from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.models import Transaction
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.routers.auth import get_current_user
from app.tasks.send_report_email import send_financial_report_email


router = APIRouter(prefix="/celery", tags=["celery"])

@router.post('/send_pdf_to_email')
async def send_pdf_email(
        session: AsyncSession = Depends(get_session),
        current_user=Depends(get_current_user)):
    query = await session.execute(
        select(Transaction).where(
            Transaction.user_id == current_user.id,
            Transaction.is_deleted == False
        )
    )
    transactions = query.scalars().all()

    tx_data = [{
        'amount': t.amount,
        'description': t.description,
        'date': t.date.strftime("%Y-%m-%d")
    }
        for t in transactions]

    send_financial_report_email.delay(
        to_email=current_user.email,
        transactions=tx_data
    )

    return {"status": "Письмо с отчётом отправлено"}