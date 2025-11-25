# fast_api_project/routers/login.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.login import LoginCreate, LoginRequest, LoginResponse
from functions import crud_login
from models.login import Login
from models.register import RegisterModel
from database import SessionLocal
import bcrypt


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


login_router = APIRouter(prefix="/auth", tags=["Login"])


# ------------------- REGISTER (Optional) -------------------
@login_router.post("/register")
def register_user(data: RegisterModel, db: Session = Depends(get_db)):
    # truncate to bcrypt-safe size
    safe_password = data.password[:72]

    hashed = crud_login.hash_password(safe_password)

    user = Login(
        email=data.email,
        password=hashed,
        role=data.role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered", "user_id": user.id}


# ------------------- LOGIN -------------------
@login_router.post("/login", response_model=LoginResponse)
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(Login).filter(Login.email == email).first()

    if not user:
        return {"msg": "Invalid email or password", "email": email, "role":user.role}

    safe_password = password[:72]

    if not bcrypt.checkpw(safe_password.encode('utf-8'), user.password.encode('utf-8')):
        return {"msg": "Invalid email or password", "email": email, "role":user.role}

    return {"msg": "Login successful", "email": user.email, "role":user.role}

