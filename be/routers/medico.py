from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from be.db import get_db
from be.models.medico import Medico
from be.schemas.medico import MedicoCreate, MedicoResponse, MedicoUpdate

router = APIRouter(prefix="/medicos", tags=["medicos"])


@router.get("", response_model=list[MedicoResponse])
def listar_medicos(db: Session = Depends(get_db)):
    return db.query(Medico).order_by(Medico.id.asc()).all()


@router.post("", response_model=MedicoResponse)
def crear_medico(data: MedicoCreate, db: Session = Depends(get_db)):
    existing = db.query(Medico).filter(Medico.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="El correo del medico ya existe.")

    medico = Medico(
        name=data.name,
        email=data.email,
        especialidad=data.especialidad or None,
    )
    db.add(medico)
    db.commit()
    db.refresh(medico)
    return medico


@router.put("/{medico_id}", response_model=MedicoResponse)
def actualizar_medico(
    medico_id: int,
    data: MedicoUpdate,
    db: Session = Depends(get_db),
):
    medico = db.get(Medico, medico_id)
    if not medico:
        raise HTTPException(status_code=404, detail="Medico no encontrado.")

    if data.name is None and data.email is None and data.especialidad is None:
        raise HTTPException(
            status_code=400,
            detail="Debes enviar al menos un campo para actualizar.",
        )

    if data.email is not None and data.email != medico.email:
        existing = db.query(Medico).filter(Medico.email == data.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="El correo del medico ya existe.")

    if data.name is not None:
        medico.name = data.name
    if data.email is not None:
        medico.email = data.email
    if data.especialidad is not None:
        medico.especialidad = data.especialidad or None

    db.commit()
    db.refresh(medico)
    return medico


@router.delete("/{medico_id}")
def eliminar_medico(medico_id: int, db: Session = Depends(get_db)):
    medico = db.get(Medico, medico_id)
    if not medico:
        raise HTTPException(status_code=404, detail="Medico no encontrado.")

    db.delete(medico)
    db.commit()
    return {"message": "Medico eliminado exitosamente."}
