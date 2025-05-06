from sqlalchemy.ext.asyncio import AsyncSession # pip install SQLAlchemy
from app.repositories.rol_repository import RolRepository
from app.schemas.rol_schema import RolSchema, RolCreateSchema, RolUpdateSchema
from app.utils.security import hash_password
from fastapi import HTTPException
from typing import List

class RolService:
    @staticmethod
    async def get_rol_by_id(db: AsyncSession, rol_id: int) -> RolSchema:
        rol = await RolRepository.get_rol_by_id(db, rol_id)
        if rol:
            return RolSchema.from_orm(rol)
        return None

    @staticmethod
    async def get_roles(db: AsyncSession) -> List[RolSchema]:
        roles = await RolRepository.get_roles(db)
        if roles:
            return [RolSchema.from_orm(rol) for rol in roles]
        return []
    
    @staticmethod
    async def create_rol(db: AsyncSession, rol_data: RolCreateSchema) -> RolSchema:
        rol_data.password = hash_password(rol_data.password)  # 🛡️ Hash de contraseña
        rol = await RolRepository.create_rol(db, rol_data)
        return RolSchema.from_orm(rol)

    @staticmethod
    async def delete_rol(db: AsyncSession, rol_id: int):
        """Desactiva un Rol cambiando su estado."""
        rol = await RolRepository.get_rol_by_id(db, rol_id)
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")

        return await RolRepository.soft_delete_rol(db, rol)
    
    @staticmethod
    async def update_rol(db: AsyncSession, rol_id: int, rol_data: RolUpdateSchema):
        """Valida y actualiza la información de un Rol."""
        rol = await RolRepository.get_rol_by_id(db, rol_id)
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")

        updated_rol = await RolRepository.update_rol(db, rol, rol_data.dict(exclude_unset=True))

        return updated_rol  # ✅ Asegúrate de devolver el Rol actualizado