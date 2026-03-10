from sqlalchemy import Column, Integer, String, Float, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Artist(Base):
    __tablename__ = "Artist"
    ArtistId = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(120))

class Album(Base):
    __tablename__ = "Album"
    AlbumId = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String(160))
    ArtistId = Column(Integer, ForeignKey("Artist.ArtistId"))

class Genre(Base):
    __tablename__ = "Genre"
    GenreId = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(120))

class Track(Base):
    __tablename__ = "Track"
    TrackId = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(200))
    AlbumId = Column(Integer, ForeignKey("Album.AlbumId"))
    GenreId = Column(Integer, ForeignKey("Genre.GenreId"))
    UnitPrice = Column(Numeric(10,2))

class Customer(Base):
    __tablename__ = "Customer"
    CustomerId = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(String(40))
    LastName = Column(String(20))
    Email = Column(String(60))

class Invoice(Base):
    __tablename__ = "Invoice"
    InvoiceId = Column(Integer, primary_key=True, autoincrement=True)
    CustomerId = Column(Integer, ForeignKey("Customer.CustomerId"))
    BillingAddress = Column(String(70), nullable=True)
    BillingCity = Column(String(40), nullable=True)
    BillingState = Column(String(40), nullable=True)
    BillingCountry = Column(String(40), nullable=True)
    BillingPostalCode = Column(String(10), nullable=True)
    InvoiceDate = Column(DateTime, nullable=True)
    Total = Column(Numeric(10,2))

class InvoiceLine(Base):
    __tablename__ = "InvoiceLine"
    InvoiceLineId = Column(Integer, primary_key=True, autoincrement=True)
    InvoiceId = Column(Integer, ForeignKey("Invoice.InvoiceId"))
    TrackId = Column(Integer, ForeignKey("Track.TrackId"))
    UnitPrice = Column(Numeric(10,2))
    Quantity = Column(Integer)
