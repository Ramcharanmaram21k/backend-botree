# botree1/schemas/officer_create.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class OfficerCreate(BaseModel):
    # Officer fields
    name: str
    email: EmailStr
    phone: str
    designation: str
    department: str
    category_expertise: str
    district: str

    mandal: Optional[str] = None
    village_ward: Optional[str] = None
    city: Optional[str] = None
    pin_code: Optional[str] = None
    max_load: Optional[int] = 10

    # Login fields
    password: str
    role: str = "officer"     # Default role

    class Config:
        from_attributes = True
