from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from app.infraestructure.db.database import engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Rol(Base):
    __tablename__ = "roles"

    id_rol = Column(Integer, primary_key=True, index=True)
    name_rol = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    modified_by = Column(String(100))
    id_fraccionamiento = Column(Integer, nullable=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)