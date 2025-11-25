# routers/grievance_tracking.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base
from models.grievance_tracking import GrievanceTracking
from schemas.grievance_tracking import (
    GrievanceTrackingCreate,
    GrievanceTrackingUpdate,
    GrievanceTrackingResponse
)
from typing import List

router = APIRouter(prefix="/grievance-tracking", tags=["Grievance Tracking"])


@router.post("/", response_model=GrievanceTrackingResponse, status_code=201)
def create_tracking(
        data: GrievanceTrackingCreate,
        db: Session = Depends(get_db)
):
    """
    Create a new grievance tracking entry.
    """
    tracking = GrievanceTracking(**data.dict())
    db.add(tracking)
    db.commit()
    db.refresh(tracking)
    return tracking


@router.get("/{tracking_id}", response_model=GrievanceTrackingResponse)
def get_tracking(tracking_id: int, db: Session = Depends(get_db)):
    """
    Get grievance tracking by ID.
    """
    tracking = db.query(GrievanceTracking).filter(GrievanceTracking.id == tracking_id).first()
    if not tracking:
        raise HTTPException(status_code=404, detail="Tracking record not found")
    return tracking


@router.get("/grievance/{grievance_id}", response_model=List[GrievanceTrackingResponse])
def get_tracking_by_grievance(grievance_id: int, db: Session = Depends(get_db)):
    """
    Get all tracking records for a specific grievance.
    """
    trackings = db.query(GrievanceTracking).filter(
        GrievanceTracking.grievance_id == grievance_id
    ).all()
    return trackings


@router.put("/{tracking_id}", response_model=GrievanceTrackingResponse)
def update_tracking(
        tracking_id: int,
        data: GrievanceTrackingUpdate,
        db: Session = Depends(get_db)
):
    """
    Update a grievance tracking record.
    """
    tracking = db.query(GrievanceTracking).filter(GrievanceTracking.id == tracking_id).first()
    if not tracking:
        raise HTTPException(status_code=404, detail="Tracking record not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(tracking, key, value)

    db.commit()
    db.refresh(tracking)
    return tracking


@router.delete("/{tracking_id}", status_code=204)
def delete_tracking(tracking_id: int, db: Session = Depends(get_db)):
    """
    Delete a grievance tracking record.
    """
    tracking = db.query(GrievanceTracking).filter(GrievanceTracking.id == tracking_id).first()
    if not tracking:
        raise HTTPException(status_code=404, detail="Tracking record not found")

    db.delete(tracking)
    db.commit()
    return None