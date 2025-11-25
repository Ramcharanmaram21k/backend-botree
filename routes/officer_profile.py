# botree1/routes/officer_profile.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.officer import Officer
from schemas.officer_profile import OfficerProfile, OfficerUpdate

router = APIRouter(prefix="/officer", tags=["Officer Profile"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------ GET OFFICER PROFILE ------------------
@router.get("/profile/{email}", response_model=OfficerProfile)
def get_officer_profile(email: str, db: Session = Depends(get_db)):
    officer = db.query(Officer).filter(Officer.email == email).first()

    if not officer:
        raise HTTPException(status_code=404, detail="Officer not found")

    return officer


# ------------------ UPDATE OFFICER PROFILE (SELF UPDATE ONLY) ------------------
@router.put("/profile/update/{email}")
def update_officer_profile(email: str, data: OfficerUpdate, db: Session = Depends(get_db)):

    officer = db.query(Officer).filter(Officer.email == email).first()

    if not officer:
        raise HTTPException(status_code=404, detail="Officer not found")

    # Officers can only update: phone, city, mandal, village_ward, pin_code
    if data.phone:
        officer.phone = data.phone
    if data.city:
        officer.city = data.city
    if data.mandal:
        officer.mandal = data.mandal
    if data.village_ward:
        officer.village_ward = data.village_ward
    if data.pin_code:
        officer.pin_code = data.pin_code

    db.commit()
    db.refresh(officer)

    return {"message": "Officer profile updated successfully"}
