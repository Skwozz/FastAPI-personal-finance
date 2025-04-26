from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app import crud_user, schemas_user, models
from app.routers.auth import get_current_user
router = APIRouter()

@router.post("/users/", response_model=schemas_user.UserRead)
async def register_user(user: schemas_user.UserCreate, session: AsyncSession = Depends(get_session)):
    existing = await crud_user.get_user_by_username(session, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")
    return await crud_user.create_user(session, user)

@router.get("/me")
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user