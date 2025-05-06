from pydantic import BaseModel, EmailStr
from typing import Any, Optional

class LoginRequest(BaseModel):
    identifier: EmailStr
    pswd: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class CustomResponse(BaseModel):
    type: str
    status: str
    message: Any