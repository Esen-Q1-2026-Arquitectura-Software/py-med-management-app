from sqlalchemy import Column, ForeignKey, Integer

from be.db import Base


class Historial(Base):
    __tablename__ = "historial"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuarioId = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    citaId = Column(Integer, ForeignKey("citas.id"), nullable=False)
    medicoId = Column(Integer, ForeignKey("medicos.id"), nullable=False)
