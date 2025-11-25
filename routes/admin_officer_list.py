# botree1/routes/admin_officer_list.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.officer import Officer
from schemas.officer_list import OfficerListResponse

router = APIRouter(prefix="/admin/officer", tags=["Admin - Officer List"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------ GET LIST OF ALL OFFICERS ------------------
@router.get("/all", response_model=list[OfficerListResponse])
def list_officers(db: Session = Depends(get_db)):

    officers = db.query(Officer).all()

    return officers
