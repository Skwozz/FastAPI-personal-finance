from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.crud import crud_category
from app.schemas import schemas_category
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

@router.delete("/categories/{category_id}", status_code= status.HTTP_204_NO_CONTENT )
async def delete_categories(
        category_id: int,

        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    category = await crud_category.delete_category(session, category_id, current_user.id)
    if not category:
        raise HTTPException(status_code=404, detail='Категория не найдена')

    return category