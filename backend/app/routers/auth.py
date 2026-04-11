from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# 🔹 Router FIRST (fixes "router not defined")
router = APIRouter(tags=["auth"])

# 🔹 Security
security = HTTPBearer()

SECRET_KEY = "yoursecretkey"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔹 PASSWORD
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# 🔹 TOKEN
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 🔹 GET CURRENT USER (must come BEFORE require_admin)
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    user = db.query(User).filter(User.email == payload["sub"]).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user

# 🔹 ADMIN CHECK
def require_admin(user=Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required ❌")
    return user

def require_hr_or_admin(user=Depends(get_current_user)):
    if user.role not in ["admin", "hr"]:
        raise HTTPException(status_code=403, detail="HR or Admin access required ❌")
    return user

# 🔹 REGISTER
# @router.post("/register")
# def register(
#     user: UserCreate,
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user)
# ):
#     if current_user.role != "admin":
#         raise HTTPException(status_code=403, detail="Only admin can create users")

#     hashed_pw = hash_password(user.password)

#     if user.role not in ["employee", "hr"]:
#         raise HTTPException(status_code=400, detail="Invalid role")

#     new_user = User(
#         email=user.email,
#         password=hashed_pw,
#         role=user.role
#     )

#     db.add(new_user)
#     db.flush() 

#     # 🔥 Auto create employee
#     if new_user.role in ["employee", "hr"]:
#         from app.models.employee import Employee

#         emp = Employee(
#             first_name=user.first_name or "New",
#             last_name=user.last_name or "User",
#             email=new_user.email,
#             user_id=new_user.id
#         )
#         db.add(emp)
#         db.commit()

#     return {"message": "User created"}
@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create users")

    if user.role not in ["employee", "hr"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    hashed_pw = hash_password(user.password)

    try:
        new_user = User(
            email=user.email,
            password=hashed_pw,
            role=user.role
        )

        db.add(new_user)
        db.flush()  # ✅ get user.id

        # 🔥 create employee
        if new_user.role in ["employee", "hr"]:
            from app.models.employee import Employee

            emp = Employee(
                first_name=user.first_name or "New",
                last_name=user.last_name or "User",
                email=new_user.email,
                user_id=new_user.id
            )
            db.add(emp)

        db.commit()  # ✅ commit BOTH together

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "User + Employee created successfully"}

# 🔹 LOGIN
@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }