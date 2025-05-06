from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.rol import Rol
from app.schemas.rol_schema import RolCreateSchema
import datetime 

class RolRepository:
    
    @staticmethod
    async def get_rol_by_id(db: AsyncSession, rol_id: int):
        query = select(Rol).where(Rol.id_rol == rol_id)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_roles(db: AsyncSession):
        query = select(Rol)
        result = await db.execute(query)
        return result.scalars().all()
    
    
    @staticmethod
    async def create_rol(db: AsyncSession, rol_data: RolCreateSchema):
        new_rol = Rol(
            name=rol_data.name,
            email=rol_data.email,
            password_hash=rol_data.password,  # ⚠️ Hash de contraseña en el servicio
            name_=rol_data.name_,
            last_name_=rol_data.last_name_,
            second_name_=rol_data.second_name_,
            phone=rol_data.phone
        )
        db.add(new_rol)
        await db.commit()
        await db.refresh(new_rol)
        return new_rol

    @staticmethod
    async def soft_delete_rol(db: AsyncSession, rol: Rol):
        """Realiza una eliminación lógica del usuario."""
        rol.status_ = False
        rol.deleted_at = datetime.datetime.utcnow()
        await db.commit()
        return rol
    
    @staticmethod
    async def update_rol(db: AsyncSession, rol: Rol, updated_data: dict):
        """Actualiza un usuario con los datos proporcionados."""
        for key, value in updated_data.items():
            if hasattr(rol, key):  # Verifica que el campo existe en el modelo
                setattr(rol, key, value)

        await db.commit()
        await db.refresh(rol)  # ✅ Refresca el usuario para devolver datos actualizados
        return rol