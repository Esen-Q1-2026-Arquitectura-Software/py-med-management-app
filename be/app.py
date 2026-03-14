import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Session

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://med-user:12345@localhost/med-management-db?charset=utf8mb4",
)

engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
    pass


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    passw = Column(String(255), nullable=False)
    med_info = Column(Text, nullable=True)


app = FastAPI()


class RegistroRequest(BaseModel):
    name: str
    email: str
    passw: str
    med_info: str = ""


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.post("/registro")
def registro(data: RegistroRequest):
    with Session(engine) as session:
        existing = session.query(Usuario).filter(Usuario.email == data.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="El correo ya está registrado.")
        usuario = Usuario(
            name=data.name,
            email=data.email,
            passw=data.passw,
            med_info=data.med_info or None,
        )
        session.add(usuario)
        session.commit()
    return {"message": "Usuario registrado exitosamente."}
