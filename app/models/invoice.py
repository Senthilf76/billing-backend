from sqlalchemy import Column, Integer, String, Date, DECIMAL, Enum
from app.database import Base
import datetime

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)

    invoice_no = Column(String(50), unique=True, index=True, nullable=True)

    customer_name = Column(String(100), nullable=True)

    date = Column(Date, default=datetime.date.today)

    subtotal = Column(DECIMAL(10, 2), nullable=True)
    gst_total = Column(DECIMAL(10, 2), nullable=True)
    transport = Column(DECIMAL(10, 2), nullable=True)
    grand_total = Column(DECIMAL(10, 2), nullable=True)

    status = Column(
        Enum("draft", "final", name="invoice_status"),
        default="draft",
        nullable=False
    )
