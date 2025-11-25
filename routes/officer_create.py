# # botree1/routes/officer_create.py

# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from database import SessionLocal
# from models.officer import Officer
# from schemas.officer_create import OfficerCreate
# from models.login import Login
# from functions.crud_login import hash_password

# router = APIRouter(prefix="/admin/officer", tags=["Admin - Officer Management"])


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @router.post("/create")
# def create_officer(data: OfficerCreate, db: Session = Depends(get_db)):

#     # Check if email exists
#     existing = db.query(Officer).filter(Officer.email == data.email).first()
#     if existing:
#         raise HTTPException(status_code=400, detail="Officer with this email already exists")

#     officer = Officer(
#         name=data.name,
#         email=data.email,
#         phone=data.phone,
#         designation=data.designation,
#         department=data.department,
#         category_expertise=data.category_expertise,
#         district=data.district,
#         mandal=data.mandal,
#         village_ward=data.village_ward,
#         city=data.city,
#         pin_code=data.pin_code,

#         is_active=True,
#         current_load=0,
#         # max_load=data.max_load
#     )

#     db.add(officer)
#     db.commit()
#     db.refresh(officer)

#     return {
#         "message": "Officer created successfully",
#         "officer_id": officer.officer_id,
#         "name": officer.name,
#         "email": officer.email,
#         "district": officer.district
#     }




# botree1/routes/officer_create.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.officer import Officer
from models.login import Login
from schemas.officer_create import OfficerCreate
from functions.crud_login import hash_password

router = APIRouter(prefix="/admin/officer", tags=["Admin - Officer Management"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create")
def create_officer(data: OfficerCreate, db: Session = Depends(get_db)):

    # Check if email exists in officer table
    existing = db.query(Officer).filter(Officer.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Officer with this email already exists")

    # Check if email exists in login table
    login_exists = db.query(Login).filter(Login.email == data.email).first()
    if login_exists:
        raise HTTPException(status_code=400, detail="Login with this email already exists")

    # Create officer in officer table
    officer = Officer(
        name=data.name,
        email=data.email,
        phone=data.phone,
        designation=data.designation,
        department=data.department,
        category_expertise=data.category_expertise,
        district=data.district,
        mandal=data.mandal,
        village_ward=data.village_ward,
        city=data.city,
        pin_code=data.pin_code,
        is_active=True,
        current_load=0,
        max_load=data.max_load
    )

    db.add(officer)
    db.flush()  # To get officer_id

    # Create login record
    hashed = hash_password(data.password)

    login_user = Login(
        email=data.email,
        password=hashed,
        role=data.role
    )

    db.add(login_user)

    db.commit()
    db.refresh(officer)

    return {
        "message": "Officer created successfully",
        "officer_id": officer.officer_id,
        "name": officer.name,
        "email": officer.email,
        "district": officer.district,
        "login_created": True
    }
