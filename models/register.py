
from typing import Annotated
from pydantic import BaseModel, StringConstraints, EmailStr

class RegisterModel(BaseModel):
    email: str
    password: Annotated[str, StringConstraints(min_length=8, max_length=72)]
    role: str
