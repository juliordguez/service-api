from fastapi import FastAPI
from app.api.v1 import users, auth, roles, fraccionamiento
from app.infraestructure.db.database import init_db
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
# pip install pydantic-settings
# pip install asyncmy
# pip install "pydantic[email]"
# pip install passlib[bcrypt]



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("⏳ Inicializando base de datos...")
    await init_db()
    print("✅ Base de datos lista.")
    yield
    print("🧹 Cerrando recursos (si fuera necesario)...")
    
app = FastAPI(title="FastAPI + MySQL Async API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Puedes poner "*" en desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(users.router, prefix="/api/v1", tags=["Users"])
app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
app.include_router(roles.router, prefix="/api/v1", tags=["Roles"])
app.include_router(fraccionamiento.router, prefix="/api/v1", tags=["Fraccionamiento"])