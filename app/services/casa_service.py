from sqlalchemy.ext.asyncio import AsyncSession # pip install SQLAlchemy
from app.repositories.fraccionamiento_repository import FraccionamientoRepository
from app.schemas.fraccionamiento_schema import FraccionamientoSchema, FraccionamientoCreateSchema, FraccionamientoUpdateSchema
from app.utils.security import hash_password
from fastapi import HTTPException
from typing import List

class FraccService:
    @staticmethod
    async def get_fraccionamiento_by_id(db: AsyncSession, fracc_id: int) -> FraccionamientoSchema:
        fracc = await FraccionamientoRepository.get_fraccionamiento_by_id(db, fracc_id)
        if fracc:
            return FraccionamientoSchema.from_orm(fracc)
        return None

    @staticmethod
    async def get_fraccionamientos(db: AsyncSession) -> List[FraccionamientoSchema]:
        fraccionamientos = await FraccionamientoRepository.get_fraccionamiento(db)
        if fraccionamientos:
            return [FraccionamientoSchema.from_orm(fraccionamiento) for fraccionamiento in fraccionamientos]
        return []
    
    @staticmethod
    async def create_fraccionamiento(db: AsyncSession, fracc_data: FraccionamientoCreateSchema) -> FraccionamientoSchema:
        fracc_data.password = hash_password(fracc_data.password)  # 🛡️ Hash de contraseña
        fracc = await FraccionamientoRepository.create_fraccionamiento(db, fracc_data)
        return FraccionamientoSchema.from_orm(fracc)

    @staticmethod
    async def delete_fraccionamiento(db: AsyncSession, fracc_id: int):
        """Desactiva un fraccionamiento cambiando su estado."""
        fracc = await FraccionamientoRepository.get_fraccionamiento_by_id(db, fracc_id)
        if not fracc:
            raise HTTPException(status_code=404, detail="Fraccionamiento no encontrado")

        return await FraccionamientoRepository.soft_delete_fraccionamiento(db, fracc)
    
    @staticmethod
    async def update_fraccionamiento(db: AsyncSession, fracc_id: int, fracc_data: FraccionamientoUpdateSchema):
        """Valida y actualiza la información de un fraccionamiento."""
        fracc = await FraccionamientoRepository.get_fraccionamiento_by_id(db, fracc_id)
        if not fracc:
            raise HTTPException(status_code=404, detail="Fraccionamiento no encontrado")

        updated_fracc = await FraccionamientoRepository.update_fraccionamiento(db, fracc, fracc_data.dict(exclude_unset=True))

        return updated_fracc  # ✅ Asegúrate de devolver el fraccionamiento actualizado