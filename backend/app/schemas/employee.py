from pydantic import BaseModel
from datetime import date
from app.schemas.leave import LeaveOut


# For creating employee
class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    department: str
    position: str
    salary: float
    hire_date: date


# For returning employee data
class EmployeeOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    department: str
    position: str
    salary: float
    hire_date: date

    leaves: list[LeaveOut] = []

    class Config:
        from_attributes = True  # important for SQLAlchemy