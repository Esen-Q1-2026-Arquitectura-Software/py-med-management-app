from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from be.config import JWT_ALGORITHM, JWT_SECRET
from be.db import get_db
from be.models.cita import Cita
from be.models.medico import Medico
from be.schemas.cita import CitaCreate, CitaResponse

router = APIRouter(prefix="/citas", tags=["citas"])

_bearer = HTTPBearer()


def _get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
) -> int:
    try:
        payload = jwt.decode(
            credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token invalido.")
        return int(user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalido.")


@router.get("", response_model=list[CitaResponse])
def listar_citas(
    db: Session = Depends(get_db),
    usuario_id: int = Depends(_get_current_user_id),
):
    rows = (
        db.query(Cita, Medico.name.label("medico_name"))
        .join(Medico, Cita.medicoId == Medico.id)
        .filter(Cita.usuarioId == usuario_id)
        .order_by(Cita.fecha.desc(), Cita.hora.desc())
        .all()
    )
    result = []
    for cita, medico_name in rows:
        result.append(
            CitaResponse(
                id=cita.id,
                usuarioId=cita.usuarioId,
                medicoId=cita.medicoId,
                fecha=cita.fecha,
                hora=cita.hora,
                motivo=cita.motivo,
                diagnostico=cita.diagnostico,
                receta=cita.receta,
                medico_name=medico_name,
            )
        )
    return result


@router.post("", response_model=CitaResponse)
def crear_cita(
    data: CitaCreate,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(_get_current_user_id),
):
    medico = db.get(Medico, data.medicoId)
    if not medico:
        raise HTTPException(status_code=404, detail="Medico no encontrado.")

    cita = Cita(
        usuarioId=usuario_id,
        medicoId=data.medicoId,
        fecha=data.fecha,
        hora=data.hora,
        motivo=data.motivo or None,
    )
    db.add(cita)
    db.commit()
    db.refresh(cita)
    return CitaResponse(
        id=cita.id,
        usuarioId=cita.usuarioId,
        medicoId=cita.medicoId,
        fecha=cita.fecha,
        hora=cita.hora,
        motivo=cita.motivo,
        diagnostico=cita.diagnostico,
        receta=cita.receta,
        medico_name=medico.name,
    )
