from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user_schema import UserCreateSchema
import datetime 

class UserRepository:
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int):
        query = select(User).where(User.id == user_id, User.status_ == 1)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_users(db: AsyncSession):
        query = select(User).where(User.status_ == 1)
        result = await db.execute(query)
        return result.scalars().all()
    

    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreateSchema):
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=user_data.password,
            name_=user_data.name_,
            last_name_=user_data.last_name_,
            second_name_=user_data.second_name_,
            phoneNumber=user_data.phoneNumber
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    @staticmethod
    async def soft_delete_user(db: AsyncSession, user: User):
        """Realiza una eliminación lógica del usuario."""
        user.status_ = False
        user.deleted_at = datetime.datetime.utcnow()
        await db.commit()
        return user
    
    @staticmethod
    async def update_user(db: AsyncSession, user: User, updated_data: dict):
        """Actualiza un usuario con los datos proporcionados."""
        for key, value in updated_data.items():
            if hasattr(user, key):  # Verifica que el campo existe en el modelo
                setattr(user, key, value)

        await db.commit()
        await db.refresh(user)  # ✅ Refresca el usuario para devolver datos actualizados
        return user