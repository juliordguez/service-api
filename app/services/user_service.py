from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserSchema, UserCreateSchema, UserUpdateSchema
from app.utils.security import hash_password
from fastapi import HTTPException
from typing import List

class UserService:
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> UserSchema:
        user = await UserRepository.get_user_by_id(db, user_id)
        if user:
            return UserSchema.from_orm(user)
        return None


    @staticmethod
    async def get_users(db: AsyncSession) -> List[UserSchema]:
        users = await UserRepository.get_users(db)
        if users:
            return [UserSchema.from_orm(user) for user in users]
        return []
    
    
    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreateSchema) -> UserSchema:
        user_data.password = hash_password(user_data.password)  # 🛡️ Hash de contraseña
        user = await UserRepository.create_user(db, user_data)
        return UserSchema.from_orm(user)

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int):
        """Desactiva un usuario cambiando su estado."""
        user = await UserRepository.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return await UserRepository.soft_delete_user(db, user)
    
    @staticmethod
    async def update_user(db: AsyncSession, user_id: int, user_data: UserUpdateSchema):
        """Valida y actualiza la información de un usuario."""
        user = await UserRepository.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        updated_user = await UserRepository.update_user(db, user, user_data.dict(exclude_unset=True))

        return updated_user  # ✅ Asegúrate de devolver el usuario actualizado