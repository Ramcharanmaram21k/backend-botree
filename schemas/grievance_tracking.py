# schemas/grievance_tracking.py
# from pydantic import BaseModel
# from typing import Optional
# from datetime import datetime
#
#
# class GrievanceTrackingCreate(BaseModel):
#     grievance_id: int
#     officer_id: Optional[int] = None
#     remarks: Optional[str] = None
#     status: str  # e.g., "Open", "In Progress", "Resolved", "Closed"
#     sla_days: int
#     sla_breached: Optional[bool] = False
#     reopened_flag: Optional[bool] = False


# class GrievanceTrackingUpdate(BaseModel):
#     officer_id: Optional[int] = None
#     remarks: Optional[str] = None
#     status: Optional[str] = None
#     resolved_at: Optional[datetime] = None
#     sla_breached: Optional[bool] = None
#     reopened_flag: Optional[bool] = None
#
#
# class GrievanceTrackingResponse(BaseModel):
#     id: int
#     grievance_id: int
#     officer_id: Optional[int]
#     remarks: Optional[str]
#     status: str
#     created_at: datetime
#     resolved_at: Optional[datetime]
#     sla_days: int
#     sla_breached: bool
#     reopened_flag: bool
#     updated_at: datetime
#
#     class Config:
#         from_attributes = True