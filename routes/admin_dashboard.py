# botree1/routes/admin_dashboard.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.grievance import Grievance
from models.citizen import Citizen
from models.media_files import MediaFile
from models.officer import Officer
from schemas.admin_dashboard import AdminGrievanceResponse, MediaFileData

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/grievances", response_model=list[AdminGrievanceResponse])
def get_all_grievances(db: Session = Depends(get_db)):

    grievances = db.query(Grievance).all()
    response = []

    for g in grievances:
        citizen = db.query(Citizen).filter(Citizen.citizen_id == g.citizen_id).first()
        media_files = db.query(MediaFile).filter(MediaFile.grievance_id == g.grievance_id).all()
        officer = db.query(Officer).filter(Officer.officer_id == g.officer_id).first()

        response.append(
            AdminGrievanceResponse(
                grievance_id=g.grievance_id,

                # citizen
                citizen_name=citizen.name,
                citizen_phone=citizen.phone,
                citizen_email=citizen.email,
                gender=citizen.gender,
                district=citizen.district,
                mandal=citizen.mandal,
                village_ward=citizen.village_ward,
                city=citizen.city,

                # grievance
                category=g.category,
                sub_category=g.sub_category,
                sentiment=g.sentiment,
                priority=g.priority,
                text_complaint=g.text_complaint,
                language=g.language,
                source_system=g.source_system,

                # officer
                officer_name=officer.name if officer else None,
                officer_department=officer.department if officer else None,
                officer_email=officer.email if officer else None,

                # media
                media_files=[
                    MediaFileData(
                        file_type=m.file_type,
                        file_path=m.file_path
                    ) for m in media_files
                ]
            )
        )

    return response
