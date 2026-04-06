from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeOut
from app.schemas import employee as employee_schema
from fastapi import HTTPException
from typing import Optional
from fastapi import Query
from sqlalchemy import or_

router = APIRouter(prefix="/employees", tags=["employees"])


# 🔥 CREATE EMPLOYEE
@router.post("/", response_model=EmployeeOut)
def create_employee(data: EmployeeCreate, db: Session = Depends(get_db)):
    emp = Employee(**data.dict())
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp

# 🔥 GET ALL EMPLOYEES

@router.get("/", response_model=list[EmployeeOut])
def get_employees(
    department: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: Optional[str] = Query("id"),
    order: Optional[str] = Query("asc"),
    limit: int = Query(10),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):
    query = db.query(Employee)

    # 🔹 Filter
    if department:
        query = query.filter(Employee.department == department)

    # 🔹 Search
    if search:
        query = query.filter(
            or_(
                Employee.first_name.ilike(f"%{search}%"),
                Employee.last_name.ilike(f"%{search}%"),
                Employee.email.ilike(f"%{search}%")
            )
        )

    # 🔹 Clean input
    sort_by = sort_by.strip() if sort_by else "id"
    order = order.strip().lower() if order else "asc"

    # 🔹 Allowed fields
    allowed_sort_fields = [
        "id", "first_name", "last_name",
        "email", "department", "position",
        "salary", "hire_date"
    ]

    if sort_by not in allowed_sort_fields:
        sort_by = "id"

    column = getattr(Employee, sort_by)

    # 🔹 Apply sorting
    if order == "desc":
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column.asc())

    # 🔥 FINAL FIX HERE
    return query.offset(offset).limit(limit).all()




# 🔥 GET ONE EMPLOYEE
@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return emp

# 🔥 UPDATE EMPLOYEE
@router.put("/{employee_id}", response_model=EmployeeOut)
def update_employee(employee_id: int, data: EmployeeCreate, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == employee_id).first()

    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    for key, value in data.dict().items():
        setattr(emp, key, value)

    db.commit()
    db.refresh(emp)
    return emp

# 🔥 DELETE EMPLOYEE
@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == employee_id).first()

    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(emp)
    db.commit()

    return {"message": "Employee deleted successfully"}

# GET employee WITH all leaves
@router.get("/{employee_id}/with-leaves", response_model=employee_schema.EmployeeOut)
def get_employee_with_leaves(employee_id: int, db: Session = Depends(get_db)):

    emp = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found ❌")

    return emp