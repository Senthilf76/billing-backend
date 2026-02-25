from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt

from app.database import SessionLocal
from app.models.user import User
from app.schemas.auth_schema import LoginRequest
from app.schemas.password_schema import PasswordResetRequest
from app.utils.security import verify_password, get_password_hash
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api", tags=["Auth"])

SECRET_KEY = "CHANGE_THIS_SECRET"
ALGORITHM = "HS256"


# -------------------------
# DB Dependency
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# LOGIN (JSON — FRONTEND SAFE)
# -------------------------
@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    token = jwt.encode(
        {
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
    }


# -------------------------
# RESET PASSWORD
# -------------------------
@router.post("/reset-password")
def reset_password(
    data: PasswordResetRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == current_user["user_id"]).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(data.current_password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Current password is incorrect",
        )

    user.password_hash = get_password_hash(data.new_password)
    db.commit()

    return {"status": "password updated successfully"}
