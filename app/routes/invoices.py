from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db
from app.models.models import Track

router = APIRouter()

class PurchaseRequest(BaseModel):
    customer_id: int
    track_id: int

@router.post("/")
def create_invoice(req: PurchaseRequest, db: Session = Depends(get_db)):
    track = db.query(Track).filter(Track.TrackId == req.track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track no encontrado")
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    price = float(track.UnitPrice)
    
    result = db.execute(text("""
        INSERT INTO Invoice (CustomerId, InvoiceDate, BillingAddress, BillingCity, BillingCountry, Total)
        VALUES (:cid, :date, 'Online', 'Online', 'Online', :total)
    """), {"cid": req.customer_id, "date": now, "total": price})
    
    invoice_id = result.lastrowid
    
    db.execute(text("""
        INSERT INTO InvoiceLine (InvoiceId, TrackId, UnitPrice, Quantity)
        VALUES (:inv_id, :track_id, :price, 1)
    """), {"inv_id": invoice_id, "track_id": req.track_id, "price": price})
    
    db.commit()
    return {"message": "Compra realizada", "invoice_id": invoice_id, "total": price}
