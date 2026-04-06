from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import get_db, engine, Base
from app.models import employee, leave  # IMPORTANT: import model
from app.routers import employees, leaves


app = FastAPI(title="HR System API")
app.include_router(employees.router)
app.include_router(leaves.router)
# 🔥 CREATE TABLES
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "HR System API is running 🚀"}

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return {"message": "Database connected successfully ✅"}