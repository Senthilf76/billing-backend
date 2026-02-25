from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from app.database import Base

class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer)
    description = Column(String(255))
    sqft = Column(DECIMAL(10,2))
    qty = Column(Integer)
    rate = Column(DECIMAL(10,2))
    gst_percent = Column(DECIMAL(5,2))
    gst_amount = Column(DECIMAL(10,2))
    final_amount = Column(DECIMAL(10,2))
