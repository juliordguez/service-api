from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.db.database import get_db
from app.services.user_service import UserService
from app.schemas.user_schema import UserSchema, UserCreateSchema, UserUpdateSchema
import datetime
from typing import List

router = APIRouter()

@router.get("/user/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.get("/user", response_model=List[UserSchema])
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await UserService.get_users(db)
    if not users:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return users

@router.post("/user/", response_model=UserSchema, status_code=201)
async def create_user(user_data: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    user = await UserService.create_user(db, user_data)
    return user

@router.delete("/user/{user_id}", response_model=dict)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Endpoint para eliminar un usuario lógicamente."""
    await UserService.delete_user(db, user_id)
    return {"message": "Usuario desactivado correctamente"}


@router.put("/user/{user_id}", response_model=UserSchema)
async def update_user(user_id: int, user_data: UserUpdateSchema, db: AsyncSession = Depends(get_db)):
    """Endpoint para actualizar un usuario."""
    updated_user = await UserService.update_user(db, user_id, user_data)
    return UserSchema.model_validate(updated_user)