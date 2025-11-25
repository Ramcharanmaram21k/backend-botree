# from pydantic import BaseModel

# class OfficerDashboardRequest(BaseModel):
#     email: str
#     password: str  

# class GrievanceItem(BaseModel):
#     grievance_id: int
#     citizen_name: str
#     phone: str
#     email: str
#     category: str
#     priority: str
#     sentiment: str
#     text_complaint: str
#     district: str
#     mandal: str
#     village_ward: str

#     class Config:
#         from_attributes = True

# botree1/schemas/officer_grievance.py
from pydantic import BaseModel

class OfficerGrievanceResponse(BaseModel):
    grievance_id: int
    citizen_name: str
    citizen_phone: str
    citizen_email: str
    category: str
    sentiment: str
    priority: str
    district: str
    mandal: str
    village_ward: str
    text_complaint: str

    class Config:
        orm_mode = True
