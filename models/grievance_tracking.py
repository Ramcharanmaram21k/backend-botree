#models/grievance_tracking.py
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.sql import func
from database import Base


class GrievanceTracking(Base):
    __tablename__ = "grievance_tracking"

    id = Column(Integer, primary_key=True, autoincrement=True)
    grievance_id = Column(Integer, ForeignKey("grievance.grievance_id", ondelete="CASCADE"), nullable=False)
    officer_id = Column(Integer, ForeignKey("officer.officer_id", ondelete="SET NULL"), nullable=True)
    remarks = Column(Text)
    status = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now())
    resolved_at = Column(TIMESTAMP, nullable=True)
    sla_days = Column(Integer)
    sla_breached = Column(Boolean, default=False)
    reopened_flag = Column(Boolean, default=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())