# botree1/routes/grievance_details.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.grievance import Grievance
from models.citizen import Citizen
from models.media_files import MediaFile
from schemas.grievance_details import GrievanceDetailResponse, MediaFileData

router = APIRouter(prefix="/grievance", tags=["Grievance Details"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{grievance_id}", response_model=GrievanceDetailResponse)
def get_grievance_details(grievance_id: int, db: Session = Depends(get_db)):

    grievance = db.query(Grievance).filter(Grievance.grievance_id == grievance_id).first()

    if not grievance:
        raise HTTPException(status_code=404, detail="Grievance not found")

    citizen = db.query(Citizen).filter(Citizen.citizen_id == grievance.citizen_id).first()

    media_files = db.query(MediaFile).filter(MediaFile.grievance_id == grievance_id).all()

    return GrievanceDetailResponse(
        grievance_id=grievance.grievance_id,

        # citizen data
        citizen_name=citizen.name,
        citizen_phone=citizen.phone,
        citizen_email=citizen.email,
        gender=citizen.gender,
        district=citizen.district,
        mandal=citizen.mandal,
        village_ward=citizen.village_ward,
        city=citizen.city,

        # grievance
        category=grievance.category,
        sub_category=grievance.sub_category,
        sentiment=grievance.sentiment,
        priority=grievance.priority,
        text_complaint=grievance.text_complaint,
        language=grievance.language,
        source_system=grievance.source_system,

        # media
        media_files=[MediaFileData(file_type=f.file_type, file_path=f.file_path) for f in media_files]
    )
