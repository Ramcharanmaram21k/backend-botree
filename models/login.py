# botree1/models/login.py
from sqlalchemy import Column, Integer, String
from database import Base

class Login(Base):
    __tablename__ = "login"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150), unique=True, index=True)
    password = Column(String(255))   # hashed password
    role = Column(String(50))
