from pydantic import BaseModel


class RegistroRequest(BaseModel):
    name: str
    email: str
    passw: str
    med_info: str = ""
