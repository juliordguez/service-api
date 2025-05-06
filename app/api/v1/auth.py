from fastapi import APIRouter, HTTPException, Response, Request, Cookie
from app.schemas.auth_schema import LoginRequest, TokenResponse, CustomResponse
from app.services.auth_services import AuthService
from fastapi.responses import JSONResponse


router = APIRouter()
auth_service = AuthService()

@router.post("/token", response_model=CustomResponse)
def login(response: Response, login_data: LoginRequest):
    token_data = auth_service.login_user(response, login_data)

    res = JSONResponse(
        status_code=201,
        content={
            "type": "Exitoso",
            "status": "201",
            "message": {
                "token": token_data.access_token
            }
        }
    )

    res.set_cookie(
        key="refresh_token",
        value=token_data.refresh_token,
        httponly=True,
        secure=False,  # ⚠️ cámbialo a True en producción
        samesite="Lax",
        path="/",
        max_age=60 * 60 * 24 * 7  # 7 días
    )

    return res

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(request: Request, refresh_token: str = Cookie(None)):
    return auth_service.refresh_tokens(refresh_token)

@router.post("/logout")
def logout(response: Response):
    return auth_service.logout_user(response)
