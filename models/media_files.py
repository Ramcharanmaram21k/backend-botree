#botree1/models/media_files.py
from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from database import Base


class MediaFile(Base):
    __tablename__ = "media_files"

    id = Column(Integer, primary_key=True, autoincrement=True)
    grievance_id = Column(Integer, ForeignKey("grievance.grievance_id", ondelete="CASCADE"))
    file_type = Column(Enum("image", "audio", "video"))
    file_path = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
