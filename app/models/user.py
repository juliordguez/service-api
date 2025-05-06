from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.infraestructure.db.database import engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name_ = Column(String(100), nullable=False)
    last_name_ = Column(String(100), nullable=False)
    second_name_ = Column(String(100), nullable=False)
    phoneNumber = Column(String(15), nullable=False)
    last_login_at = Column(DateTime, nullable=True)
    force_password_change = Column(Boolean, default=False)
    
    deleted_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    status_ = Column(Boolean, default=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
