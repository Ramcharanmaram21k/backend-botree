# from pydantic import BaseModel
#
#
# class SubmitRequest(BaseModel):
#     # Citizen
#     name: str
#     phone: str
#     email: str
#     gender: str
#     address: str
#     city: str
#     state: str
#     country: str
from pydantic import BaseModel

class SubmitRequest(BaseModel):
    # Citizen fields
    name: str
    phone: str
    email: str
    gender: str
    district: str
    mandal: str
    village_ward: str
    city: str

    # Grievance
    source_system: str
    language: str
    text_complaint: str
    # latitude: float | None = None
    # longitude: float | None = None
    category: str
    sub_category: str
    priority: str
    sentiment: str
    # Grievance fields
    text_complaint: str

