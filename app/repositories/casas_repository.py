from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.casa import Casa
from app.schemas.casa_schema import casaCreateSchema
import datetime

class casasRepository:
    @staticmethod
    
    async def get_casa_by_id(db: AsyncSession, casa_id: int):
        query = select(Casa).where(Casa.id_casa == casa_id)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_casas(db: AsyncSession):
        query = select(Casa)
        result = await db.execute(query)
        return result.scalars().all()
    
    
    @staticmethod
    async def create_casas(db: AsyncSession, casas_data: casaCreateSchema):
        new_casa = Casa(
            name_casa=casas_data.name_casa,
            updated_at=casas_data.updated_at,
            modified_by=casas_data.modified_by,
        )
        db.add(new_casa)
        await db.commit()
        await db.refresh(new_casa)
        return new_casa

    @staticmethod
    async def soft_delete_casas(db: AsyncSession, casa: Casa):
        """Realiza una eliminación lógica del usuario."""
        casa.estatus = False
        casa.deleted_at = datetime.datetime.utcnow()
        await db.commit()
        return casa
    
    @staticmethod
    async def update_casas(db: AsyncSession, casa: Casa, updated_data: dict):
        """Actualiza un usuario con los datos proporcionados."""
        for key, value in updated_data.items():
            if hasattr(casa, key):  # Verifica que el campo existe en el modelo
                setattr(casa, key, value)

        await db.commit()
        await db.refresh(casa)  # ✅ Refresca el usuario para devolver datos actualizados
        return casa