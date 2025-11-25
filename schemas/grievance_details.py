# botree1/schemas/grievance_details.py
from pydantic import BaseModel
from typing import List, Optional

class MediaFileData(BaseModel):
    file_type: str
    file_path: str

    class Config:
        orm_mode = True


class GrievanceDetailResponse(BaseModel):
    grievance_id: int

    # citizen
    citizen_name: str
    citizen_phone: str
    citizen_email: str
    gender: str
    district: str
    mandal: str
    village_ward: str
    city: str

    # grievance
    category: str
    sub_category: str
    sentiment: str
    priority: str
    text_complaint: str
    language: str
    source_system: str

    # media
    media_files: List[MediaFileData]

    class Config:
        from_attributes = True
