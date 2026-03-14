from sqlalchemy import Column, Integer, String

from be.db import Base


class Medico(Base):
    __tablename__ = "medicos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    especialidad = Column(String(255), nullable=True)
