from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Configuración del motor asíncrono para MySQL con pool de conexiones
DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    pool_size=10,        # Número máximo de conexiones en el pool
    max_overflow=20,     # Número máximo de conexiones adicionales
    pool_recycle=1800,   # Tiempo antes de reciclar conexiones (evita desconexiones)
    pool_timeout=30      # Tiempo máximo de espera para obtener una conexión
)

# Sesión asíncrona con pool de conexiones
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)

# Dependencia de sesión
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(lambda session: None)  # Inicializa la conexión

# Dependencia para obtener sesiones de BD
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session