from datetime import date, time
from typing import Literal

from pydantic import BaseModel, ConfigDict


EstadoCita = Literal[
    "pendiente",
    "confirmada",
    "completada",
    "finalizada",
    "cancelada",
]


class CitaCreate(BaseModel):
    medicoId: int
    fecha: date
    hora: time
    estado: EstadoCita = "pendiente"
    motivo: str | None = None


class CitaEstadoUpdate(BaseModel):
    estado: EstadoCita


class CitaResponse(BaseModel):
    id: int
    usuarioId: int
    medicoId: int
    fecha: date
    hora: time
    estado: EstadoCita
    motivo: str | None
    diagnostico: str | None
    receta: str | None
    medico_name: str | None = None

    model_config = ConfigDict(from_attributes=True)
