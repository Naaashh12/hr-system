from pydantic import BaseModel
from datetime import date
from app.schemas.leave import LeaveOut
from typing import Optional



# For creating employee
class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    department: str
    position: str
    salary: float
    hire_date: date

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    salary: Optional[float] = None
    hire_date: Optional[date] = None

# For returning employee data
class EmployeeOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    department: Optional[str] = None
    position: Optional[str] = None
    salary: Optional[float] = None
    user_id: Optional[int] = None

    leaves: list[LeaveOut] = []

    class Config:
        from_attributes = True  # important for SQLAlchemy