# botree1/routes/admin_officer_profile.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.officer import Officer
from schemas.officer_profile import OfficerProfile, AdminOfficerUpdate

router = APIRouter(prefix="/admin/officer", tags=["Admin - Officer Profile"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------ ADMIN GET OFFICER PROFILE ------------------
@router.get("/profile/{email}", response_model=OfficerProfile)
def admin_get_officer_profile(email: str, db: Session = Depends(get_db)):
    officer = db.query(Officer).filter(Officer.email == email).first()

    if not officer:
        raise HTTPException(status_code=404, detail="Officer not found")

    return officer


# ------------------ ADMIN UPDATE OFFICER PROFILE ------------------
@router.put("profile/update/{email}")
def admin_update_officer(email: str, data: AdminOfficerUpdate, db: Session = Depends(get_db)):

    officer = db.query(Officer).filter(Officer.email == email).first()

    if not officer:
        raise HTTPException(status_code=404, detail="Officer not found")

    # Admin can update ALL fields
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(officer, field, value)

    db.commit()
    db.refresh(officer)

    return {"message": "Officer details updated by Admin successfully"}
