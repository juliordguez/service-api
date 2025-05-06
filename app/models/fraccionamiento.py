from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from app.infraestructure.db.database import engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Fraccionamiento(Base):
    __tablename__ = "fraccionamientos"

    id_fraccionamiento = Column(Integer, primary_key=True, index=True)
    name_fraccionamiento = Column(String(100), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    modified_by = Column(String(100))
    
# class Fraccionamiento(Base):
#     __tablename__ = "fraccionamientos"

#     id = Column(Integer, primary_key=True, index=True)
#     nombre = Column(String(150), nullable=False)
#     descripcion = Column(Text, nullable=True)
#     direccion = Column(String(255), nullable=True)
#     municipio = Column(String(100), nullable=True)
#     estado = Column(String(100), nullable=True)
#     codigo_postal = Column(String(10), nullable=True)
#     referencias = Column(Text, nullable=True)

#     responsable_nombre = Column(String(150), nullable=True)
#     responsable_telefono = Column(String(20), nullable=True)
#     responsable_email = Column(String(150), nullable=True)

#     estatus = Column(Boolean, default=True)         # Activo o inactivo
#     eliminado = Column(Boolean, default=False)       # Eliminado lógico

#     creado_por = Column(String(100), nullable=True)
#     fecha_creacion = Column(DateTime, default=func.now())
#     actualizado_por = Column(String(100), nullable=True)
#     fecha_actualizacion = Column(DateTime, nullable=True)
#     eliminado_por = Column(String(100), nullable=True)
#     fecha_eliminacion = Column(DateTime, nullable=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
