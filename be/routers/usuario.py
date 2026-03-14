from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from jose import jwt
from sqlalchemy.orm import Session

from be.config import JWT_ALGORITHM, JWT_EXPIRE_MINUTES, JWT_SECRET
from be.db import get_db
from be.models.usuario import Usuario
from be.schemas.usuario import LoginRequest, RegistroRequest, TokenResponse

router = APIRouter()


@router.post("/registro")
def registro(data: RegistroRequest, db: Session = Depends(get_db)):
    existing = db.query(Usuario).filter(Usuario.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")
    usuario = Usuario(
        name=data.name,
        email=data.email,
        passw=data.passw,
        med_info=data.med_info or None,
    )
    db.add(usuario)
    db.commit()
    return {"message": "Usuario registrado exitosamente."}


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == data.email).first()
    if not usuario or usuario.passw != data.passw:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos.")
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload = {
        "sub": str(usuario.id),
        "email": usuario.email,
        "name": usuario.name,
        "exp": expire,
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=JWT_EXPIRE_MINUTES * 60,
        name=usuario.name,
    )
