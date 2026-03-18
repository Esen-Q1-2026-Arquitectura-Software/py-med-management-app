from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text, Time

from be.db import Base


class Cita(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuarioId = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    medicoId = Column(Integer, ForeignKey("medicos.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    estado = Column(String(30), nullable=False, default="pendiente", server_default="pendiente")
    motivo = Column(Text, nullable=True)
    diagnostico = Column(Text, nullable=True)
    receta = Column(Text, nullable=True)
