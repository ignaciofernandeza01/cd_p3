# models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from db import Base
from werkzeug.security import generate_password_hash, check_password_hash


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(120), nullable=False, unique=True)  # título
    foto = Column(Text)             # ruta o URL de imagen
    link = Column(Text)             # URL oficial
    descripcion = Column(Text)
    popularidad = Column(Integer)   # 1..5
    trailer = Column(Text)
    categoria = Column(String(80))  # Acción, Deportes, etc.
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def set_password(self, pwd: str):
        self.password_hash = generate_password_hash(pwd)

    def check_password(self, pwd: str) -> bool:
        return check_password_hash(self.password_hash, pwd)