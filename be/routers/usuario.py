from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from be.db import get_db
from be.models.usuario import Usuario
from be.schemas.usuario import RegistroRequest

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
