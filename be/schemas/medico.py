from pydantic import BaseModel, ConfigDict


class MedicoBase(BaseModel):
    name: str
    email: str
    especialidad: str | None = None


class MedicoCreate(MedicoBase):
    pass


class MedicoUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    especialidad: str | None = None


class MedicoResponse(MedicoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
