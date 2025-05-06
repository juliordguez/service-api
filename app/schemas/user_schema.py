from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    name_: str
    last_name_: str
    second_name_: str
    phoneNumber: str
    last_login_at: datetime | None = None
    status_: bool
    
    class Config:
        from_attributes  = True #orm_mode es pasado

class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str  # ⚠️ Guardar con hash en `user_service.py`
    name_: str
    last_name_: str
    second_name_: str
    phoneNumber: str
    
class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    name_: Optional[str] = None
    last_name_: Optional[str] = None
    second_name_: Optional[str] = None
    phoneNumber: Optional[str] = None

    class Config:
        from_attributes = True  # Para convertir de SQLAlchemy a Pydantic