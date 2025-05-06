from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.db.database import get_db
from app.services.rol_service import RolService
from app.schemas.rol_schema import RolSchema, RolCreateSchema, RolUpdateSchema
import datetime
from typing import List

router = APIRouter()

@router.get("/rol/{rol_id}", response_model=RolSchema)
async def get_rol(rol_id: int, db: AsyncSession = Depends(get_db)):
    rol = await RolService.get_rol_by_id(db, rol_id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol


@router.get("/roles", response_model=List[RolSchema])
async def get_roles(db: AsyncSession = Depends(get_db)):
    roles = await RolService.get_roles(db)
    if not roles:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return roles


@router.post("/rol/", response_model=RolSchema, status_code=201)
async def create_rol(rol_data: RolCreateSchema, db: AsyncSession = Depends(get_db)):
    rol = await RolService.create_rol(db, rol_data)
    return rol

@router.delete("/rol/{rol_id}", response_model=dict)
async def delete_rol(rol_id: int, db: AsyncSession = Depends(get_db)):
    """Endpoint para eliminar un Rol lógicamente."""
    await RolService.delete_rol(db, rol_id)
    return {"message": "Rol desactivado correctamente"}


@router.put("/rol/{rol_id}", response_model=RolSchema)
async def update_rol(rol_id: int, rol_data: RolUpdateSchema, db: AsyncSession = Depends(get_db)):
    """Endpoint para actualizar un Rol."""
    updated_rol = await RolService.update_rol(db, rol_id, rol_data)
    return RolSchema.model_validate(updated_rol)