from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import leave as leave_model
from app.models import employee as employee_model
from app.schemas import leave as leave_schema

router = APIRouter(prefix="/leaves", tags=["Leaves"])


@router.post("/", response_model=leave_schema.LeaveOut)
def create_leave(leave: leave_schema.LeaveCreate, db: Session = Depends(get_db)):
    
    # ✅ CHECK: employee exists
    employee = db.query(employee_model.Employee).filter(
        employee_model.Employee.id == leave.employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found ❌")

    new_leave = leave_model.Leave(**leave.dict(), status="pending")

    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)

    return new_leave

@router.get("/", response_model=list[leave_schema.LeaveOut])
def get_all_leaves(status: str = None, db: Session = Depends(get_db)):

    query = db.query(leave_model.Leave)

    if status:
        query = query.filter(leave_model.Leave.status == status)

    return query.all()

@router.get("/{leave_id}", response_model=leave_schema.LeaveOut)
def get_leave(leave_id: int, db: Session = Depends(get_db)):
    
    leave = db.query(leave_model.Leave).filter(
        leave_model.Leave.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found ❌")

    return leave

@router.put("/{leave_id}/status", response_model=leave_schema.LeaveOut)
def update_leave_status(
    leave_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    leave = db.query(leave_model.Leave).filter(
        leave_model.Leave.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found ❌")

    leave.status = status

    db.commit()
    db.refresh(leave)

    return leave