from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import get_db, engine, Base
from app.models import employee, leave  # IMPORTANT: import model
from app.routers import employees, leaves
from app.routers import auth
from app.models import user 
from app.routers import dashboard

from fastapi.middleware.cors import CORSMiddleware

import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(title="HR System API")
app.include_router(employees.router)
app.include_router(leaves.router)
app.include_router(auth.router, prefix="/auth")
app.include_router(dashboard.router)
# 🔥 CREATE TABLES
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "HR System API is running 🚀"}

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return {"message": "Database connected successfully ✅"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # allow React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)