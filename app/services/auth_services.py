from fastapi import HTTPException, Response
from datetime import timedelta
from jose import JWTError # pip install python-jose
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.utils.security import create_token, decode_token
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from app.infraestructure.db_fake import FAKE_DB

class AuthService:

    def login_user(self, response: Response, login_data: LoginRequest) -> TokenResponse:
        user = FAKE_DB.get(login_data.identifier)
        if not user or user["pswd"] != login_data.pswd:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        user_data = {"sub": login_data.identifier, "user_id": user["user_id"]}
        access_token = create_token(user_data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        refresh_token = create_token(user_data, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

        # Ya no seteamos la cookie aquí, lo hará el endpoint
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    def refresh_tokens(self, refresh_token: str) -> TokenResponse:
        if not refresh_token:
            raise HTTPException(status_code=401, detail="No se encontró el refresh token")

        try:
            payload = decode_token(refresh_token)
            user_data = {"sub": payload.get("sub"), "user_id": payload.get("user_id")}

            new_access_token = create_token(user_data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
            new_refresh_token = create_token(user_data, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

            response = Response()
            response.set_cookie(
                key="refresh_token",
                value=new_refresh_token,
                httponly=True,
                secure=True,
                samesite="strict"
            )
            return TokenResponse(access_token=new_access_token)

        except JWTError:
            raise HTTPException(status_code=401, detail="Refresh token inválido")

    def logout_user(self, response: Response):
        response.delete_cookie("refresh_token")
        return {"message": "Sesión cerrada correctamente"}
