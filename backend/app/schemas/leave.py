from pydantic import BaseModel
from datetime import date


class LeaveCreate(BaseModel):
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: str


class LeaveOut(BaseModel):
    id: int
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    status: str
    reason: str

    class Config:
        from_attributes = True