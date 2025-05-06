from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from app.infraestructure.db.database import engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Casa(Base):
    __tablename__ = "casas"

    id_casa = Column(Integer, primary_key=True, index=True)
    name_casa = Column(String(100), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    modified_by = Column(String(100))
    

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)