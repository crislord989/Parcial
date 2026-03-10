from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import tracks, customers, invoices

app = FastAPI(title="Chinook API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tracks.router, prefix="/api/tracks", tags=["Tracks"])
app.include_router(customers.router, prefix="/api/customers", tags=["Customers"])
app.include_router(invoices.router, prefix="/api/invoices", tags=["Invoices"])

@app.get("/")
def root():
    return {"message": "Chinook API funcionando"}
