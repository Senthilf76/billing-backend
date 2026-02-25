from pydantic import BaseModel, Field
from typing import List, Optional
import datetime

class InvoiceItemCreate(BaseModel):
    description: Optional[str] = None
    sqft: Optional[float] = None
    qty: Optional[int] = None
    rate: Optional[float] = None
    gst: Optional[float] = 0
    gst_amount: Optional[float] = 0
    final_amount: Optional[float] = None

class InvoiceCreate(BaseModel):
    customer_name: Optional[str] = None
    date: Optional[datetime.date] = Field(default_factory=datetime.date.today)
    subtotal: Optional[float] = None
    gst_total: Optional[float] = 0
    transport: Optional[float] = 0
    grand_total: Optional[float] = None
    items: Optional[List[InvoiceItemCreate]] = []
