# botree1/schemas/officer_list.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class OfficerListResponse(BaseModel):
    officer_id: int
    name: str
    email: EmailStr
    phone: Optional[str]
    designation: Optional[str]
    department: Optional[str]
    category_expertise: Optional[str]
    district: Optional[str]
    mandal: Optional[str]
    village_ward: Optional[str]
    city: Optional[str]
    pin_code: Optional[str]
    max_load: Optional[int]
    current_load: Optional[int]
    is_active: Optional[bool]

    class Config:
        from_attributes = True
