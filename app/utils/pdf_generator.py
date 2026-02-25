from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

def generate_invoice_pdf(invoice, items, file_path):
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    y = height - 30 * mm

    c.setFont("Helvetica-Bold", 14)
    c.drawString(30 * mm, y, "TAX INVOICE")

    y -= 15 * mm
    c.setFont("Helvetica", 10)
    c.drawString(30 * mm, y, f"Invoice No: {invoice.invoice_no}")
    y -= 5 * mm
    c.drawString(30 * mm, y, f"Date: {invoice.date}")

    y -= 10 * mm
    c.drawString(30 * mm, y, f"Customer: {invoice.customer_name}")

    y -= 15 * mm
    c.drawString(30 * mm, y, "Items:")

    y -= 8 * mm
    for item in items:
        c.drawString(30 * mm, y, f"- {item.description} | Qty: {item.qty} | Rate: {item.rate}")
        y -= 6 * mm

    y -= 10 * mm
    c.drawString(30 * mm, y, f"Subtotal: {invoice.subtotal}")
    y -= 5 * mm
    c.drawString(30 * mm, y, f"GST Total: {invoice.gst_total}")
    y -= 5 * mm
    c.drawString(30 * mm, y, f"Grand Total: {invoice.grand_total}")

    c.showPage()
    c.save()
