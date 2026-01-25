from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from jose import jwt
from fastapi import Header, HTTPException
from app.database import SessionLocal
from app.models.invoice import Invoice

router = APIRouter(prefix="/api/gst", tags=["GST"])

SECRET_KEY = "CHANGE_THIS_SECRET"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Header(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing token"
        )
def admin_only(user):
    if user.get("role") != "admin":
        raise HTTPException(403, "Admin access required")

@router.get("/monthly")
def monthly_gst_report(
    year: int,
    month: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    admin_only(user)

    result = db.execute(
        text("""
            SELECT
                SUM(subtotal) AS total_taxable,
                SUM(gst_total) AS total_gst,
                SUM(grand_total) AS total_amount
            FROM invoices
            WHERE status = 'final'
              AND YEAR(date) = :year
              AND MONTH(date) = :month
        """),
        {"year": year, "month": month}
    ).fetchone()

    return {
        "year": year,
        "month": month,
        "total_taxable": result[0] or 0,
        "total_gst": result[1] or 0,
        "total_amount": result[2] or 0,
    }
