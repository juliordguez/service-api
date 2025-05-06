from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.db.database import get_db
from app.services.fraccionamiento_service import FraccService
from app.schemas.fraccionamiento_schema import FraccionamientoSchema, FraccionamientoCreateSchema, FraccionamientoUpdateSchema
import datetime
from typing import List

router = APIRouter()

@router.get("/fraccionamiento/{fracc_id}", response_model=FraccionamientoSchema)
async def get_fraccionamiento_by_id(fracc_id: int, db: AsyncSession = Depends(get_db)):
    fraccionamiento = await FraccService.get_fraccionamiento_by_id(db, fracc_id)
    if not fraccionamiento:
        raise HTTPException(status_code=404, detail="Fraccionamiento no encontrado")
    return fraccionamiento

@router.get("/fraccionamientos", response_model=List[FraccionamientoSchema])
async def get_fraccionamientos(db: AsyncSession = Depends(get_db)):
    fraccionamientos = await FraccService.get_fraccionamientos(db)
    if not fraccionamientos:
        raise HTTPException(status_code=404, detail="Fraccionamiento no encontrado")
    return fraccionamientos


@router.post("/fraccionamiento/", response_model=FraccionamientoSchema, status_code=201)
async def create_fraccionamiento(fraccionamiento_data: FraccionamientoCreateSchema, db: AsyncSession = Depends(get_db)):
    fraccionamiento = await FraccService.create_fraccionamiento(db, fraccionamiento_data)
    return fraccionamiento

@router.delete("/fraccionamiento/{fraccionamiento_id}", response_model=dict)
async def delete_fraccionamiento(fraccionamiento_id: int, db: AsyncSession = Depends(get_db)):
    """Endpoint para eliminar un Fraccionamiento lógicamente."""
    await FraccService.delete_fraccionamiento(db, fraccionamiento_id)
    return {"message": "Fraccionamiento desactivado correctamente"}


@router.put("/fraccionamiento/{fracc_id}", response_model=FraccionamientoSchema)
async def update_fraccionamiento(fracc_id: int, fracc_data: FraccionamientoUpdateSchema, db: AsyncSession = Depends(get_db)):
    """Endpoint para actualizar un Fraccionamiento."""
    updated_fraccionamiento = await FraccService.update_fraccionamiento(db, fracc_id, fracc_data)
    return FraccionamientoSchema.model_validate(updated_fraccionamiento)