from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app import crud_category, schemas_category
from app.routers.auth import get_current_user
from app.models import User
router = APIRouter()

@router.post("/categories/", response_model=schemas_category.CategoryRead)
async def create_category(
    category: schemas_category.CategoryCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await crud_category.create_category(session, category, user_id=current_user.id)

@router.get("/categories/", response_model=list[schemas_category.CategoryRead])
async def read_categories(
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    return await crud_category.get_categories(session, user_id=current_user.id)
