from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Customer

router = APIRouter()

@router.get("/")
def get_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer).all()
    return [{"id": c.CustomerId, "name": f"{c.FirstName} {c.LastName}", "email": c.Email} for c in customers]
