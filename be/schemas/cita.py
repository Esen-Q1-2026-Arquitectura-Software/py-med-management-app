from datetime import date, time

from pydantic import BaseModel, ConfigDict


class CitaCreate(BaseModel):
    medicoId: int
    fecha: date
    hora: time
    motivo: str | None = None


class CitaResponse(BaseModel):
    id: int
    usuarioId: int
    medicoId: int
    fecha: date
    hora: time
    motivo: str | None
    diagnostico: str | None
    receta: str | None
    medico_name: str | None = None

    model_config = ConfigDict(from_attributes=True)
