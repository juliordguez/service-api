from fastapi import FastAPI, HTTPException, Depends, Response, Request, Cookie
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from jose import JWTError, jwt

# Configuración de seguridad
SECRET_KEY = "MI_CLAVE_SUPER_SECRETA"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

app = FastAPI()

# Base de datos simulada (ejemplo)
FAKE_DB = {
    "usuario@example.com": {
        "password": "123456",  # ⚠️ En producción usa hashing seguro
        "user_id": 1
    }
}

# Modelo de entrada para login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Modelo de respuesta para tokens
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Función para generar tokens
def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# **LOGIN: Autenticación y generación de tokens**
@app.post("/token", response_model=TokenResponse)
def login(response: Response, login_data: LoginRequest):
    user = FAKE_DB.get(login_data.email)
    if not user or user["password"] != login_data.password:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    user_data = {"sub": login_data.email, "user_id": user["user_id"]}
    
    # Generar tokens
    access_token = create_token(user_data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_token(user_data, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    # Guardar refresh token en cookie segura
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,  # Protege contra JavaScript
        secure=True,    # Solo HTTPS en producción
        samesite="strict"
    )

    return {"access_token": access_token, "token_type": "bearer"}

# **REFRESH TOKEN: Generar nuevos tokens usando la cookie**
@app.post("/refresh", response_model=TokenResponse)
def refresh_token(request: Request, refresh_token: str = Cookie(None)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No se encontró el refresh token")

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_data = {"sub": payload.get("sub"), "user_id": payload.get("user_id")}

        new_access_token = create_token(user_data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        new_refresh_token = create_token(user_data, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

        # Actualizar cookie con nuevo refresh token
        response = Response()
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            secure=True,
            samesite="strict"
        )

        return {"access_token": new_access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Refresh token inválido")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8193, reload=True)


# aiohappyeyeballs==2.6.1
# aiohttp==3.11.18
# aiomysql==0.2.0
# aioodbc==0.5.0
# aiosignal==1.3.2
# aiosqlite==0.21.0
# annotated-types==0.7.0
# anyio==4.9.0
# 
# attrs==25.3.0
# bcrypt==4.3.0
# certifi==2025.1.31
# cffi==1.17.1
# chardet==5.2.0
# charset-normalizer==3.4.1
# click==8.1.8
# colorama==0.4.6
# contourpy==1.3.1
# cryptography==44.0.2
# cycler==0.12.1
# dnspython==2.7.0
# ecdsa==0.19.1
# email_validator==2.2.0

# fonttools==4.57.0
# frozenlist==1.6.0
# greenlet==3.2.1
# h11==0.16.0
# httptools==0.6.4
# idna==3.10
# joblib==1.4.2
# jsonpickle==4.0.5
# kiwisolver==1.4.8
# loguru==0.7.3
# matplotlib==3.10.1
# more-itertools==10.6.0
# multidict==6.4.3
# music21==9.5.0
# mysql==0.0.3
# mysql-connector-python==9.3.0
# mysqlclient==2.2.7
# numpy==1.26.4
# packaging==24.2

# pillow==11.2.1
# playwright==1.52.0
# propcache==0.3.1
# pyasn1==0.4.8
# pycparser==2.22

# pyee==13.0.0
# PyMySQL==1.1.1
# pyodbc==5.2.0
# pyparsing==3.2.3
# python-dateutil==2.9.0.post0
# python-dotenv==1.1.0

# pytz==2025.2
# PyYAML==6.0.2
# requests==2.32.3
# rsa==4.9.1
# six==1.17.0
# sniffio==1.3.1

# starlette==0.46.2

# urllib3==2.4.0
# watchfiles==1.0.5
# webcolors==24.11.1
# websockets==15.0.1
# win32_setctime==1.2.0
# yarl==1.20.0