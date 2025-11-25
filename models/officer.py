#botree1/models/officer.py
from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Officer(Base):
    __tablename__ = "officer"

    officer_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100))
    department = Column(String(100))
    category_expertise = Column(String(100))
    city = Column(String(100))
    is_active = Column(Boolean, default=True)
    current_load = Column(Integer, default=0)
    #officer_id = Column("Officer_id", Integer, primary_key=True, index=True, autoincrement=True)
    #name = Column(String(255))
    phone = Column(String(20))
    email = Column(String(255))
    designation = Column(String(100))
    # category_expertise = Column(String(100))
    # department = Column(String(100))
    #city = Column(String(100))
    pin_code = Column(String(20))
    district = Column(String(100))
    mandal = Column(String(100))
    village_ward = Column(String(100))
    is_active = Column(Boolean, default=True)
    current_load = Column(Integer, default=0)
    max_load = Column(Integer, default=10)
