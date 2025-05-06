from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class FraccionamientoSchema(BaseModel):
    id_fraccionamiento: int
    name_fraccionamiento: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    modified_by: Optional[str]

    class Config:
        from_attributes = True  # Pydantic v2
        
class FraccionamientoCreateSchema(BaseModel):
    name_fraccionamiento: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    modified_by: Optional[str]

    class Config:
        from_attributes = True  # Pydantic v2
        
class FraccionamientoUpdateSchema(BaseModel):
    name_fraccionamiento: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    modified_by: Optional[str]

    class Config:
        from_attributes = True  # Pydantic v2