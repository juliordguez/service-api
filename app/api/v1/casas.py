from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.db.database import get_db
from app.services.casa_service import casasService
from app.schemas.casa_schema import casasSchema, casasCreateSchema, casasUpdateSchema
import datetime
from typing import List

router = APIRouter()

@router.get("/casas/{casas_id}", response_model=casasSchema)
async def get_casas(casas_id: int, db: AsyncSession = Depends(get_db)):
    casas = await casasService.get_casas_by_id(db, casas_id)
    if not casas:
        raise HTTPException(status_code=404, detail="casas no encontrado")
    return casas


@router.get("/casas", response_model=List[casasSchema])
async def get_casas(db: AsyncSession = Depends(get_db)):
    casas = await casasService.get_casas(db)
    if not casas:
        raise HTTPException(status_code=404, detail="casas no encontrado")
    return casas


@router.post("/casas/", response_model=casasSchema, status_code=201)
async def create_casas(casas_data: casasCreateSchema, db: AsyncSession = Depends(get_db)):
    casas = await casasService.create_casas(db, casas_data)
    return casas

@router.delete("/casas/{casas_id}", response_model=dict)
async def delete_casas(casas_id: int, db: AsyncSession = Depends(get_db)):
    """Endpoint para eliminar un casas lógicamente."""
    await casasService.delete_casas(db, casas_id)
    return {"message": "casas desactivado correctamente"}


@router.put("/casas/{casas_id}", response_model=casasSchema)
async def update_casas(casas_id: int, casas_data: casasUpdateSchema, db: AsyncSession = Depends(get_db)):
    """Endpoint para actualizar un casas."""
    updated_casas = await casasService.update_casas(db, casas_id, casas_data)
    return casasSchema.model_validate(updated_casas)