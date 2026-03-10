from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.models.models import Track, Album, Artist, Genre

router = APIRouter()

@router.get("/")
def get_tracks(q: str = Query(None), db: Session = Depends(get_db)):
    query = db.query(Track).join(Album).join(Artist).join(Genre, isouter=True)
    if q:
        query = query.filter(or_(
            Track.Name.ilike(f"%{q}%"),
            Artist.Name.ilike(f"%{q}%"),
            Genre.Name.ilike(f"%{q}%")
        ))
    tracks = query.limit(50).all()
    return [{"id": t.TrackId, "name": t.Name, "price": t.UnitPrice} for t in tracks]
