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



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    try:
        if not verify_password(data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid username or password")
    except Exception:
        # handles corrupted / legacy hashes safely
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = jwt.encode(
        {"user_id": user.id, "role": user.role},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return {
        "access_token": token,
        "role": user.role,
    }



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
        raise HTTPException(status_code=401, detail="Current password is incorrect")

    user.password_hash = get_password_hash(data.new_password)
    db.commit()

    return {"status": "password updated successfully"}



@router.post("/reset-admin-temp")
def reset_admin_temp(db: Session = Depends(get_db)):
    admin = db.query(User).filter(User.username == "admin").first()

    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    admin.password_hash = get_password_hash("admin123")
    db.commit()

    return {"status": "admin password reset"}

