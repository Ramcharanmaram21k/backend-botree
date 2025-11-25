# botree1/schemas/officer_profile.py

from pydantic import BaseModel, EmailStr
from typing import Optional

class OfficerProfile(BaseModel):
    officer_id: int
    name: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    designation: Optional[str] = None
    department: Optional[str] = None
    category_expertise: Optional[str] = None
    district: Optional[str] = None
    mandal: Optional[str] = None
    village_ward: Optional[str] = None
    city: Optional[str] = None
    pin_code: Optional[str] = None
    max_load: Optional[int] = None
    is_active: Optional[bool] = None
    current_load: Optional[int] = None

    class Config:
        from_attributes = True

class OfficerUpdate(BaseModel):
    phone: Optional[str] = None
    city: Optional[str] = None
    mandal: Optional[str] = None
    village_ward: Optional[str] = None
    pin_code: Optional[str] = None

    class Config:
        from_attributes = True


class AdminOfficerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    designation: Optional[str] = None
    department: Optional[str] = None
    category_expertise: Optional[str] = None
    district: Optional[str] = None
    mandal: Optional[str] = None
    village_ward: Optional[str] = None
    city: Optional[str] = None
    pin_code: Optional[str] = None
    max_load: Optional[int] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True
