#botree1/models/citizen.py
from sqlalchemy import Column, Integer, String,Text
from database import Base

class Citizen(Base):
    __tablename__ = "citizen"

    citizen_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    phone = Column(String(20))
    email = Column(String(255))
    gender = Column(String(20))
    district = Column(Text)
    mandal = Column(Text)
    village_ward = Column(Text)
    city = Column(String(255))

