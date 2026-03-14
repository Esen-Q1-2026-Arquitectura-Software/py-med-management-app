from sqlalchemy import Column, Date, ForeignKey, Integer, Text, Time

from be.db import Base


class Cita(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuarioId = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    medicoId = Column(Integer, ForeignKey("medicos.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    motivo = Column(Text, nullable=True)
    diagnostico = Column(Text, nullable=True)
    receta = Column(Text, nullable=True)
