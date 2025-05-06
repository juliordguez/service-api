from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

        
class casaSchema(BaseModel):
    id_casa: int
    name_casa: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    modified_by: Optional[str]

    class Config:
        from_attributes = True  # Pydantic v2
        
class casaCreateSchema(BaseModel):
    name_casa: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    modified_by: Optional[str]

    class Config:
        from_attributes = True  # Pydantic v2
        
class casaUpdateSchema(BaseModel):
    name_casa: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    modified_by: Optional[str]

    class Config:
        from_attributes = True  # Pydantic v2