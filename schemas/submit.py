from pydantic import BaseModel


class SubmitRequest(BaseModel):
    # Citizen
    name: str
    phone: str
    email: str
    gender: str
    address: str
    city: str
    state: str
    country: str

    # Grievance
    source_system: str
    language: str
    text_complaint: str
    latitude: float | None = None
    longitude: float | None = None
    category: str
    sub_category: str
    priority: str
    sentiment: str
