from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

    
# --- Rol completo (para respuestas) ---
class RolSchema(BaseModel):
    id_rol: int
    name_rol: str
    description: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    modified_by: Optional[str]
    id_fraccionamiento: int

    class Config:
        from_attributes  = True

# --- Para crear un Rol ---
class RolCreateSchema(BaseModel):
    name_: str
    descripcion: Optional[str] = None

# --- Para actualizar un Rol ---
class RolUpdateSchema(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True  # ORM compatibility
        