from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from datetime import datetime
from typing import List
from app.database import get_db

router = APIRouter()

class InvoiceItem(BaseModel):
    track_id: int
    unit_price: float
    quantity: int = 1

class PurchaseRequest(BaseModel):
    customer_id: int
    items: List[InvoiceItem]

@router.post("/")
def create_invoice(req: PurchaseRequest, db: Session = Depends(get_db)):
    if not req.items:
        raise HTTPException(status_code=400, detail="Sin canciones")

    total = sum(i.unit_price * i.quantity for i in req.items)
    now   = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Obtener el siguiente InvoiceId manualmente
    result = db.execute(text("SELECT COALESCE(MAX(InvoiceId), 0) + 1 FROM Invoice"))
    invoice_id = result.scalar()

    db.execute(text("""
        INSERT INTO Invoice (InvoiceId, CustomerId, InvoiceDate, BillingAddress, BillingCity, BillingCountry, Total)
        VALUES (:inv_id, :cid, :date, 'Online', 'Online', 'Online', :total)
    """), {"inv_id": invoice_id, "cid": req.customer_id, "date": now, "total": total})

    for item in req.items:
        result2 = db.execute(text("SELECT COALESCE(MAX(InvoiceLineId), 0) + 1 FROM InvoiceLine"))
        line_id = result2.scalar()
        db.execute(text("""
            INSERT INTO InvoiceLine (InvoiceLineId, InvoiceId, TrackId, UnitPrice, Quantity)
            VALUES (:line_id, :inv_id, :track_id, :price, :qty)
        """), {"line_id": line_id, "inv_id": invoice_id, "track_id": item.track_id,
               "price": item.unit_price, "qty": item.quantity})

    db.commit()
    return {"message": "Compra realizada", "invoice_id": invoice_id, "total": round(total, 2)}
