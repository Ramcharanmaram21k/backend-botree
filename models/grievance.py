from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from database import Base


class Grievance(Base):
    __tablename__ = "grievance"

    grievance_id = Column(Integer, primary_key=True, index=True)
    citizen_id = Column(Integer, ForeignKey("citizen.citizen_id"), nullable=False)

    source_system = Column(String(50))
    language = Column(String(50))
    text_complaint = Column(Text)

    category = Column(String(255))
    sub_category = Column(String(255))
    priority = Column(String(50))
    sentiment = Column(String(50))


    district = Column(Text)
    mandal = Column(Text)
    village_ward = Column(Text)
    city = Column(String(255))



