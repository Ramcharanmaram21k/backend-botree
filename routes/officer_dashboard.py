# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from database import SessionLocal
# from models.officer import Officer
# from models.grievance import Grievance
# from models.citizen import Citizen
# from schemas.officer_dashboard import OfficerDashboardRequest, GrievanceItem

# router = APIRouter(prefix="/officer", tags=["Officer Dashboard"])


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @router.post("/dashboard", response_model=list[GrievanceItem])
# def get_officer_grievances(data: OfficerDashboardRequest, db: Session = Depends(get_db)):

#     # 1️⃣ Fetch officer record
#     officer = db.query(Officer).filter(Officer.officer_id == data.officer_id).first()

#     if not officer:
#         raise HTTPException(status_code=404, detail="Officer not found")

#     # 2️⃣ Fetch grievances matching officer location + category
#     grievance_query = (
#         db.query(
#             Grievance.grievance_id,
#             Citizen.name.label("citizen_name"),
#             Citizen.phone,
#             Citizen.email,
#             Grievance.category,
#             Grievance.priority,
#             Grievance.sentiment,
#             Grievance.text_complaint,
#             Grievance.district,
#             Grievance.mandal,
#             Grievance.village_ward,
#         )
#         .join(Citizen, Citizen.citizen_id == Grievance.citizen_id)
#         .filter(
#             Grievance.category == officer.category_expertise,
#             Grievance.district == officer.district,
#             Grievance.mandal == officer.mandal,
#             Grievance.village_ward == officer.village_ward,
#             Grievance.officer_id == officer.officer_id,   # 🟢 Best practice
#         )
#         .all()
#     )

#     return grievance_query





from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.officer import Officer
from models.grievance import Grievance
from models.citizen import Citizen
from schemas.officer_dashboard import OfficerGrievanceResponse
# from routes.officer_dashboard import

router = APIRouter(prefix="/officer", tags=["Officer Dashboard"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/grievances/{email}", response_model=list[OfficerGrievanceResponse])
def get_officer_grievances(email: str, db: Session = Depends(get_db)):

    officer = db.query(Officer).filter(Officer.email == email).first()

    if not officer:
        raise HTTPException(status_code=404, detail="Officer not found")

    # MATCH BASED ON CATEGORY + LOCATION
    grievances = (
        db.query(
            Grievance.grievance_id,
            Citizen.name.label("citizen_name"),
            Citizen.phone.label("citizen_phone"),
            Citizen.email.label("citizen_email"),
            Grievance.category,
            Grievance.sentiment,
            Grievance.priority,
            Grievance.district,
            Grievance.mandal,
            Grievance.village_ward,
            Grievance.text_complaint
        )
        .join(Citizen, Citizen.citizen_id == Grievance.citizen_id)
        .filter(
            Grievance.category == officer.category_expertise,
            Grievance.district == officer.district,
            Grievance.mandal == officer.mandal,
            Grievance.village_ward == officer.village_ward
        )
        .all()
    )

    return grievances
