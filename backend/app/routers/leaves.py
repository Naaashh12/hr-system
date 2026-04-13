from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import leave as leave_model
from app.models import employee as employee_model
from app.schemas import leave as leave_schema
from app.routers.auth import get_current_user, require_hr   # add import at top if missing


router = APIRouter(prefix="/leaves", tags=["Leaves"])

@router.get("/my-leaves", response_model=list[leave_schema.LeaveOut])
def get_my_leaves(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    emp = db.query(employee_model.Employee).filter(
        employee_model.Employee.user_id == user.id
    ).first()

    if not emp:
        raise HTTPException(status_code=404, detail="Employee not linked")

    return emp.leaves

@router.get("/pending", response_model=list[leave_schema.LeaveOut])
def get_pending_leaves(
    db: Session = Depends(get_db),
    user=Depends(require_hr)
):
    return db.query(leave_model.Leave).filter(
        leave_model.Leave.status == "pending"
    ).all()

@router.post("/", response_model=leave_schema.LeaveOut)
def create_leave(
    leave: leave_schema.LeaveCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.role != "employee":
        raise HTTPException(status_code=403, detail="Only employees can apply for leave ❌")
    # ✅ CHECK: employee exists
    employee = db.query(employee_model.Employee).filter(
    employee_model.Employee.user_id == user.id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not linked ❌")

    new_leave = leave_model.Leave(
    **leave.dict(),
    employee_id=employee.id,
    status="pending"
)

    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)

    return new_leave

@router.get("/", response_model=list[leave_schema.LeaveOut])
def get_all_leaves(
    status: str = None,
    db: Session = Depends(get_db),
    user=Depends(require_hr)
):

    query = db.query(leave_model.Leave)

    if status:
        query = query.filter(leave_model.Leave.status == status)

    return query.all()

@router.put("/{leave_id}/status", response_model=leave_schema.LeaveOut)
def update_leave_status(
    leave_id: int,
    data: leave_schema.LeaveStatusUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_hr)
):
    leave = db.query(leave_model.Leave).filter(
        leave_model.Leave.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found ❌")

    if data.status not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    leave.status = data.status

    db.commit()
    db.refresh(leave)

    return leave

@router.get("/{leave_id}", response_model=leave_schema.LeaveOut)
def get_leave(leave_id: int, db: Session = Depends(get_db)):
    
    leave = db.query(leave_model.Leave).filter(
        leave_model.Leave.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found ❌")

    return leave


