from sqlalchemy import Column, Integer, String, Text

from be.db import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    passw = Column(String(255), nullable=False)
    med_info = Column(Text, nullable=True)
