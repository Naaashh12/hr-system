from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeOut, EmployeeUpdate
from app.schemas import employee as employee_schema
from typing import Optional
from sqlalchemy import or_ 
from app.routers.auth import get_current_user, require_admin, require_hr
import logging

router = APIRouter(prefix="/employees", tags=["employees"])
logger = logging.getLogger(__name__)
# Browser sends HTTP request
#         ↓
# Uvicorn (server receives request)
#         ↓
# FastAPI (finds matching route)
#         ↓
# Router ("/employees/" + POST)
#         ↓
# Pydantic Schema (EmployeeCreate validates data)
#         ↓
# Function runs (create_employee)
#         ↓
# SQLAlchemy Model created
#         ↓
# Session writes to DB
#         ↓
# Response converted using EmployeeOut
#         ↓
# Returned to browser

# 🔥 CREATE EMPLOYEE
@router.post("/", response_model=EmployeeOut)
def create_employee(
    data: EmployeeCreate,
    db: Session = Depends(get_db),
    user=Depends(require_admin)    # ✅ PROTECTED
    
):
    emp = Employee(**data.dict())
    db.add(emp)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Create failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")
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
    offset: int = Query(0), #how many records to skip before starting to return data
    db: Session = Depends(get_db),#Dependency injection for DB session
    user=Depends(get_current_user)   # ✅ PROTECTED
):
    query = db.query(Employee).filter(Employee.is_active == True) #Base query to get all employees

    # 🔹 Filter
    if department: #SELECT * FROM employees WHERE department = 'Engineering'
        query = query.filter(Employee.department == department)

    # 🔹 Search
    if search:
        query = query.filter(
            or_(
                Employee.first_name.ilike(f"%{search}%"), #WHERE first_name ILIKE '%nash%'
                Employee.last_name.ilike(f"%{search}%"),  #OR last_name ILIKE '%nash%'
                Employee.email.ilike(f"%{search}%")       #OR email ILIKE '%nash%'
            )
        )

    # 🔹 Clean input
    sort_by = sort_by.strip() if sort_by else "id"      #Removes spaces + normalizes input
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

    return query.offset(offset).limit(limit).all() #Pagination using offset and limit


# 🔥 GET ONE EMPLOYEE
@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)   # ✅ PROTECTED
):
    emp = db.query(Employee).filter(
    Employee.id == employee_id,
    Employee.is_active == True
).first()

    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    return emp


# 🔥 UPDATE EMPLOYEE
@router.patch("/{employee_id}", response_model=EmployeeOut)
def patch_employee(
    employee_id: int,
    data: EmployeeUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_hr)
):
    logger.info(f"Updating employee {employee_id} with data {data.dict(exclude_unset=True)}")

    emp = db.query(Employee).filter(Employee.id == employee_id).first()

    if not emp:
        logger.warning(f"Employee {employee_id} not found")
        raise HTTPException(status_code=404, detail="Employee not found")
    # key = "first_name", value = "Nashrat"
    # setattr(emp, "first_name", "Nashrat")

    # key = "department", value = "AI"
    # setattr(emp, "department", "AI")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(emp, key, value)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Update failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")
    db.refresh(emp)

    logger.info(f"Employee {employee_id} updated successfully")

    return emp


# 🔥 DELETE EMPLOYEE
@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_admin)   # ✅ PROTECTED
):
    emp = db.query(Employee).filter(Employee.id == employee_id).first()

    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    emp.is_active = False

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Delete failed for employee {employee_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")

    return {"message": "Employee deleted successfully"}


# 🔥 GET employee WITH leaves
@router.get("/{employee_id}/with-leaves", response_model=employee_schema.EmployeeOut)
def get_employee_with_leaves(
    employee_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)   # ✅ PROTECTED
):
    emp = db.query(Employee).filter(Employee.id == employee_id).first()

    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found ❌")

    return emp