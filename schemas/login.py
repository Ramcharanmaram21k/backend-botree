
from pydantic import BaseModel, EmailStr, constr, StringConstraints
from typing import Annotated

class LoginBase(BaseModel):
    email: str

class LoginCreate(LoginBase):
    password: Annotated[str, StringConstraints(max_length=72)]
    role: str

class LoginResponse(BaseModel):
    msg: str
    email: str
    role: str


class LoginRequest(BaseModel):
    email: str
    password: str
    # role: str
