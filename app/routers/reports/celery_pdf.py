from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_session
from app.routers.auth import get_current_user
from app.models import Transaction
from app.utils.pdf_generator import generate_pdf

from tempfile import NamedTemporaryFile

router = APIRouter(prefix="/celery", tags=["celery"])


@router.get('/pdf/',response_class= FileResponse)
async def export_pdf(
        session: AsyncSession = Depends(get_session),
        current_user= Depends(get_current_user)):
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

    pdf_buffer = generate_pdf(tx_data)

    with NamedTemporaryFile(delete=False,prefix='.pdf') as tmp:
        tmp.write(pdf_buffer.read())
        tmp_path = tmp.name

    return FileResponse(
        path=tmp_path,
        filename='report_pdf',
        media_type='application/pdf'
    )