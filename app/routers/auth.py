from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt

from app.database import SessionLocal
from app.models.user import User
from app.utiles.security import verify_password
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

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = jwt.encode(
        {"user_id": user.id, "role": user.role},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": token,
        "role": user.role
    }
