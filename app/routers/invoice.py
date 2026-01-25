from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from jose import jwt

from app.database import SessionLocal
from app.schemas.invoice_schema import InvoiceCreate
from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem
from fastapi.responses import FileResponse
import os
from app.utiles.pdf_generator import generate_invoice_pdf


router = APIRouter(prefix="/api/invoices", tags=["Invoices"])

# 🔐 JWT CONFIG (must match auth.py)
SECRET_KEY = "CHANGE_THIS_SECRET"
ALGORITHM = "HS256"

# -----------------------------
# DB Dependency
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# Auth Dependency (TOKEN HEADER)
# -----------------------------
def get_current_user(token: str = Header(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # contains user_id, role
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing token"
        )

# -----------------------------
# Admin-only check
# -----------------------------
def admin_only(user):
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

# -----------------------------
# SAVE INVOICE (DRAFT – PROTECTED)
# -----------------------------
@router.post("/")
def save_invoice(
    data: InvoiceCreate,
    user=Depends(get_current_user),   # 🔑 TOKEN REQUIRED
    db: Session = Depends(get_db)
):
    invoice = Invoice(
        invoice_no=f"INV-{date.today().strftime('%Y%m%d')}",
        customer_name=data.customer_name,
        date=data.date,
        subtotal=data.subtotal,
        gst_total=data.gst_total,
        transport=data.transport,
        grand_total=data.grand_total,
        status="draft"   # 🔑 important for GST flow
    )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    if data.items:
        for item in data.items:
            db.add(
                InvoiceItem(
                    invoice_id=invoice.id,
                    description=item.description,
                    sqft=item.sqft,
                    qty=item.qty,
                    rate=item.rate,
                    gst_percent=item.gst,
                    gst_amount=item.gst_amount,
                    final_amount=item.final_amount
                )
            )

    db.commit()

    return {
        "invoice_id": invoice.id,
        "invoice_no": invoice.invoice_no,
        "status": invoice.status,
        "created_by": user["user_id"]
    }

# -----------------------------
# FINALIZE INVOICE (ADMIN ONLY)
# -----------------------------
@router.post("/{invoice_id}/finalize")
def finalize_invoice(
    invoice_id: int,
    user=Depends(get_current_user),   # 🔑 login required
    db: Session = Depends(get_db)
):
    # 🔒 ADMIN CHECK
    admin_only(user)

    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    if invoice.status == "final":
        raise HTTPException(status_code=400, detail="Invoice already finalized")

    # ✅ GST SAFETY CHECKS
    if not invoice.customer_name:
        raise HTTPException(400, "Customer name missing")

    if invoice.subtotal is None:
        raise HTTPException(400, "Subtotal missing")

    if invoice.gst_total is None:
        raise HTTPException(400, "GST total missing")

    if invoice.grand_total is None:
        raise HTTPException(400, "Grand total missing")

    invoice.status = "final"
    db.commit()
    

    return {
        "message": "Invoice finalized successfully",
        "invoice_id": invoice.id,
        "invoice_no": invoice.invoice_no
    }
@router.get("/{invoice_id}/pdf")
def download_invoice_pdf(
    invoice_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    # ❌ BLOCK DRAFT PDFs
    if invoice.status != "final":
        raise HTTPException(
            status_code=400,
            detail="Invoice not finalized. PDF not available."
        )

    items = db.query(InvoiceItem).filter(
        InvoiceItem.invoice_id == invoice.id
    ).all()

    os.makedirs("invoices", exist_ok=True)
    file_path = f"invoices/{invoice.invoice_no}.pdf"

    generate_invoice_pdf(invoice, items, file_path)

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=f"{invoice.invoice_no}.pdf"
    )
