from pydantic import BaseModel


class RegistroRequest(BaseModel):
    name: str
    email: str
    passw: str
    med_info: str = ""


class LoginRequest(BaseModel):
    email: str
    passw: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
    name: str
