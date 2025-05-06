from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.fraccionamiento import Fraccionamiento
from app.schemas.fraccionamiento_schema import FraccionamientoCreateSchema
import datetime 

class FraccionamientoRepository:
    @staticmethod
    
    async def get_fraccionamiento_by_id(db: AsyncSession, fracc_id: int):
        query = select(Fraccionamiento).where(Fraccionamiento.id_fraccionamiento == fracc_id)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_fraccionamiento(db: AsyncSession):
        query = select(Fraccionamiento)
        result = await db.execute(query)
        return result.scalars().all()
    
    
    @staticmethod
    async def create_fraccionamiento(db: AsyncSession, fraccionamiento_data: FraccionamientoCreateSchema):
        new_fracc = Fraccionamiento(
            name_fraccionamiento=fraccionamiento_data.name_fraccionamiento,
            updated_at=fraccionamiento_data.updated_at,
            modified_by=fraccionamiento_data.modified_by,  # ⚠️ Hash de contraseña en el servicio
        )
        db.add(new_fracc)
        await db.commit()
        await db.refresh(new_fracc)
        return new_fracc

    @staticmethod
    async def soft_delete_fraccionamiento(db: AsyncSession, fracc: Fraccionamiento):
        """Realiza una eliminación lógica del usuario."""
        fracc.d = datetime.datetime.utcnow()
        await db.commit()
        return fracc
    
    @staticmethod
    async def update_fraccionamiento(db: AsyncSession, fracc: Fraccionamiento, updated_data: dict):
        """Actualiza un usuario con los datos proporcionados."""
        for key, value in updated_data.items():
            if hasattr(fracc, key):  # Verifica que el campo existe en el modelo
                setattr(fracc, key, value)

        await db.commit()
        await db.refresh(fracc)  # ✅ Refresca el usuario para devolver datos actualizados
        return fracc