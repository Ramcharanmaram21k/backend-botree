# fast_api_project/crud/crud_login.py
from sqlalchemy.orm import Session
from models.login import Login
from schemas.login import LoginCreate
from passlib.context import CryptContext
import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def create_user(db: Session, data: LoginCreate):
    hashed_pass = hash_password(data.password)
    db_user = Login(email=data.email, password=hashed_pass, role=data.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str, role: str):
    user = db.query(Login).filter(Login.email == email).first()
    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    # Case-insensitive role match
    if user.role.lower() != role.lower():
        return None

    return user


def hash_password(password: str) -> str:
    # bcrypt max limit = 72 bytes → safe truncate
    password = password[:72]
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")