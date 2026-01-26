from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt

from app.database import SessionLocal
from app.models.user import User
from app.utils.security import verify_password, get_password_hash
from app.schemas.auth_schema import LoginRequest

router = APIRouter(prefix="/api", tags=["Auth"])

SECRET_KEY = "CHANGE_THIS_SECRET"
ALGORITHM = "HS256"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# LOGIN ENDPOINT (STABLE)
# =========================
@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    try:
        valid = verify_password(data.password, user.password_hash)
    except Exception:
        # if hash is old/corrupted → avoid 500
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not valid:
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


# =================================================
# TEMPORARY — REMOVE AFTER SUCCESSFUL LOGIN
# =================================================
@router.post("/reset-admin-temp")
def reset_admin_temp(db: Session = Depends(get_db)):
    admin = db.query(User).filter(User.username == "admin").first()

    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    admin.password_hash = get_password_hash("admin123")
    db.commit()

    return {"status": "admin password reset"}
