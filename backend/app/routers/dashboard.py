from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.employee import Employee
from app.models.leave import Leave   # ✅ correct import
from app.routers.auth import require_admin

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/admin")
def admin_dashboard(
    db: Session = Depends(get_db),
    user=Depends(require_admin)
):
    total_employees = db.query(Employee).count()
    total_leaves = db.query(Leave).count()
    pending_leaves = db.query(Leave).filter(Leave.status == "pending").count()

    return {
        "total_employees": total_employees,
        "total_leaves": total_leaves,
        "pending_leaves": pending_leaves
    }