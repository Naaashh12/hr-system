Senior Engineer's Roadmap for Beginners
Build an AI-Powered
HR System
A complete baby-steps guide — system design, architecture, code, and everything you need to build it from scratch.

FastAPI Backend
React Frontend
AI Chatbot
PostgreSQL
Docker
Claude API

#00 — OVERVIEW
What Are We Building?
An HR (Human Resources) system is software that companies use to manage their employees. Think of it like the brain of an office — it tracks who works there, their salaries, leave days, performance, and more. We'll add an AI chatbot on top so employees can ask questions like "How many leave days do I have left?" and get instant answers.

Module	What It Does	Tech Used
👤 Employee Management	Add, edit, view, remove employees	FastAPIPostgreSQL
🔐 Auth System	Login, logout, roles (Admin, HR, Employee)	JWTbcrypt
🏖 Leave Management	Apply for leave, approve/reject	FastAPIReact
💰 Payroll	Track salary, generate payslips	FastAPIPostgreSQL
📊 Performance	Set goals, submit reviews	ReactFastAPI
🤖 AI Chatbot	Answer HR questions in natural language	Claude APILangChain
📧 Notifications	Email alerts for leave, payroll, etc.	SMTPRedis

01 — ARCHITECTURE

System Design Architecture
This is the big picture — all the pieces of our system and how they talk to each other. Don't worry, we'll explain each one.

Users 💼HR Manager Web Browser 👤EmployeeWeb Browser ⚙️AdminWeb Browser
↕ HTTP / HTTPS Requests
Frontend⚛️React AppVite + TailwindCSS🤖Chat UIReact Component 📊DashboardRecharts
↕ REST API calls (fetch / axios)
Gateway
🚪
API Gateway / NginxRoutes traffic · SSL · Rate Limiting
↕
Backend
🔐
Auth ServiceFastAPI + JWT 👥 HR ServiceFastAPI 💬 AI Chat ServiceFastAPI + Claude 📧 Notification ServiceCelery + SMTP
↕
Data 🐘PostgreSQLMain Database ⚡RedisCache + Queue 📁File StorageS3 / Local 🧠Vector DBPinecone / pgvector
↕
External
🤖
Claude APIAnthropic AI
📨
Email (SMTP)SendGrid / Gmail
🐳
DockerContainerization
Baby Step Tip: Think of the architecture like a restaurant. Users = customers, Frontend = menu/waiter, Backend = kitchen, Database = pantry/fridge, AI = a smart chef's assistant. Everything has a role!


02 — TECH STACK

Tools & Technologies
Here's every tool you'll use and why. As a beginner, don't try to learn all at once — just know what each one does.

⚛️
Frontend
React
Builds the UI. Like HTML but smarter — you build reusable "components".
🎨
Styling
Tailwind CSS
Makes your app look good without writing much CSS. Use class names directly in HTML.
⚡
Backend
FastAPI
Python framework to build your REST API. Very beginner-friendly with automatic docs.
🐘
Database
PostgreSQL
Where all your data lives — employees, salaries, leaves. Like a smart Excel sheet.
🔗
ORM
SQLAlchemy
Lets you talk to your database using Python instead of raw SQL queries.
🔐
Auth
JWT + bcrypt
JWT = login tokens. bcrypt = safely stores hashed passwords. Standard security.
⚡
Cache
Redis
Super fast key-value store. Used for caching data and background task queues.
🤖
AI
Claude API
Anthropic's AI that powers your chatbot. Send it a question, get a smart answer back.
🐳
DevOps
Docker
Packages your whole app into containers. Works the same on any computer.
📊
DB Migrations
Alembic
Tracks and applies changes to your database schema over time. Like Git for your DB.
📦
Task Queue
Celery
Runs tasks in the background (like sending emails) without slowing down your API.
🧠
AI Framework
LangChain
Helps connect your AI to your database so the chatbot can answer HR-specific questions.

03 — PROJECT STRUCTURE
Folder Structure
This is how you'll organize your project files. Good structure = easy to find things = less headaches.

hr-system/ — Project Root
hr-system/
├── backend/                     # FastAPI Python backend
│   ├── app/
│   │   ├── main.py              # App entry point
│   │   ├── config.py            # Settings (DB URL, API keys)
│   │   ├── database.py          # DB connection setup
│   │   ├── models/              # Database table definitions
│   │   │   ├── employee.py
│   │   │   ├── leave.py
│   │   │   ├── payroll.py
│   │   │   └── user.py
│   │   ├── schemas/             # Data validation (what data looks like)
│   │   │   ├── employee.py
│   │   │   └── leave.py
│   │   ├── routers/             # API endpoints (the URLs)
│   │   │   ├── auth.py          # /auth/login, /auth/register
│   │   │   ├── employees.py     # /employees/
│   │   │   ├── leaves.py        # /leaves/
│   │   │   ├── payroll.py       # /payroll/
│   │   │   └── chatbot.py       # /chat/
│   │   ├── services/            # Business logic (the brain)
│   │   │   ├── auth_service.py
│   │   │   ├── employee_service.py
│   │   │   └── ai_service.py    # Claude API integration
│   │   └── utils/               # Helper functions
│   ├── alembic/                 # Database migration files
│   ├── requirements.txt         # Python dependencies
│   └── Dockerfile
│
├── frontend/                    # React frontend
│   ├── src/
│   │   ├── pages/               # Full page components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Employees.jsx
│   │   │   ├── Leaves.jsx
│   │   │   └── Chatbot.jsx
│   │   ├── components/          # Reusable UI pieces
│   │   │   ├── Navbar.jsx
│   │   │   ├── Table.jsx
│   │   │   └── ChatWidget.jsx
│   │   ├── api/                 # API call functions
│   │   │   └── index.js
│   │   └── App.jsx              # Main app router
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml           # Run everything together
└── README.md

04 — DATABASE
Database Design (Tables)
Your database has tables, like spreadsheets. Each table stores one type of data. Here are the key tables:

backend/app/models/employee.py
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id         = Column(Integer, primary_key=True)      # Unique ID for each employee
    first_name = Column(String, nullable=False)         # Cannot be empty
    last_name  = Column(String, nullable=False)
    email      = Column(String, unique=True)            # No duplicates
    department = Column(String)
    position   = Column(String)
    salary     = Column(Float)
    hire_date  = Column(Date)
    manager_id = Column(Integer, ForeignKey("employees.id")) # Self-reference

    # Relationships — SQLAlchemy links tables together
    leaves     = relationship("Leave", back_populates="employee")
    payrolls   = relationship("Payroll", back_populates="employee")


class Leave(Base):
    __tablename__ = "leaves"

    id          = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    leave_type  = Column(String)         # "sick", "annual", "unpaid"
    start_date  = Column(Date)
    end_date    = Column(Date)
    status      = Column(String, default="pending")  # pending/approved/rejected
    reason      = Column(String)

    employee    = relationship("Employee", back_populates="leaves")
05 — BACKEND
Backend API — Key Code Snippets
These are real working examples. Read them carefully — each line is explained.

backend/app/main.py — App Entry Point
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, employees, leaves, payroll, chatbot

app = FastAPI(title="HR System API", version="1.0")

# Allow React frontend to talk to our API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all API routes
app.include_router(auth.router,      prefix="/auth")
app.include_router(employees.router, prefix="/employees")
app.include_router(leaves.router,    prefix="/leaves")
app.include_router(payroll.router,   prefix="/payroll")
app.include_router(chatbot.router,   prefix="/chat")

@app.get("/")
def root():
    return {"message": "HR System API is running! 🚀"}
backend/app/routers/employees.py — Employee Endpoints
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeOut

router = APIRouter(tags=["employees"])

# GET all employees — http://localhost:8000/employees/
@router.get("/", response_model=list[EmployeeOut])
def get_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()

# GET one employee — http://localhost:8000/employees/5
@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

# POST create employee — http://localhost:8000/employees/
@router.post("/", response_model=EmployeeOut, status_code=201)
def create_employee(data: EmployeeCreate, db: Session = Depends(get_db)):
    emp = Employee(**data.dict())
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp
backend/app/routers/chatbot.py — AI Chatbot Endpoint
import anthropic
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.employee import Employee, Leave
from app.config import settings

router = APIRouter(tags=["chatbot"])
client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

class ChatMessage(BaseModel):
    message: str
    employee_id: int  # Who is asking?

@router.post("/message")
def chat(payload: ChatMessage, db: Session = Depends(get_db)):
    # 1. Fetch relevant data from DB to give to Claude as context
    emp = db.query(Employee).filter(Employee.id == payload.employee_id).first()
    leaves = db.query(Leave).filter(Leave.employee_id == payload.employee_id).all()

    # 2. Build context string for Claude
    context = f"""
    Employee: {emp.first_name} {emp.last_name}
    Department: {emp.department}
    Leave history: {[{l.leave_type: l.status} for l in leaves]}
    """

    # 3. Call Claude API with context + user question
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=f"""You are a helpful HR assistant. Answer the employee's
        question based on this context: {context}. Be concise and friendly.""",
        messages=[{"role": "user", "content": payload.message}]
    )
    return {"reply": response.content[0].text}
06 — BUILD ROADMAP
Your Week-by-Week Roadmap
Build this in phases. Don't jump ahead — finish each phase fully before moving on.

WEEK 1–2
Phase 1 — Setup & Foundation
Get your environment ready and understand the basics. This is the hardest part mentally — push through it!
Install Python 3.11+
Install Node.js 18+
Install Docker Desktop
Install VS Code
Learn Git basics (init, add, commit, push)
Create GitHub repo
Set up FastAPI hello world
Set up React app with Vite
WEEK 3–4
Phase 2 — Database & Models
Design your database tables and connect FastAPI to PostgreSQL. Learn SQLAlchemy and Alembic migrations.
Run PostgreSQL with Docker
Create Employee, Leave, Payroll models
Set up Alembic migrations
Run first migration (create tables)
Test DB connection in FastAPI
WEEK 5–6
Phase 3 — Authentication
Build login/register system with hashed passwords and JWT tokens. Security first!
POST /auth/register endpoint
POST /auth/login → returns JWT token
Password hashing with bcrypt
JWT middleware (protect routes)
Role-based access (admin vs employee)
WEEK 7–9
Phase 4 — Core HR APIs
Build all the main CRUD endpoints for employees, leaves, and payroll.
Employee CRUD (Create/Read/Update/Delete)
Leave apply + approve/reject flow
Payroll record creation
Performance reviews endpoint
Test all endpoints with FastAPI Swagger UI
WEEK 10–12
Phase 5 — React Frontend
Build the UI. Create all pages, connect them to your API using axios/fetch.
Login page + JWT storage
Employee list + add/edit forms
Leave management dashboard
Payroll page with tables
Charts for HR analytics (Recharts)
WEEK 13–14
Phase 6 — 🤖 AI Chatbot
The exciting part! Connect Claude API to your backend and build the chat UI in React.
Get Anthropic API key
Build /chat/message endpoint
Pass employee DB context to Claude
React ChatWidget component
Floating chat button on all pages
Streaming responses (typewriter effect)
WEEK 15–16
Phase 7 — Docker & Polish
Package everything in Docker, add email notifications, do final testing.
Write Dockerfiles for frontend + backend
docker-compose.yml (run all services)
Email notifications with Celery
Environment variables (.env file)
Deploy to a VPS (optional)
07 — COMMANDS
Terminal Commands — Start Here Today
Copy and run these exactly. They set up your entire project from scratch.

Terminal — Run these commands one by one
# 1. Create project folder
mkdir hr-system && cd hr-system

# 2. Set up backend
mkdir backend && cd backend
python -m venv venv                   # Create virtual environment
source venv/bin/activate              # Activate it (Mac/Linux)
# venv\Scripts\activate              # Windows version

# 3. Install Python packages
pip install fastapi uvicorn sqlalchemy psycopg2-binary
pip install alembic python-jose[cryptography] passlib[bcrypt]
pip install python-dotenv anthropic pydantic-settings
pip freeze > requirements.txt         # Save all dependencies

# 4. Run FastAPI dev server
uvicorn app.main:app --reload         # Opens at http://localhost:8000
# Visit http://localhost:8000/docs for auto-generated API docs!

# 5. In a NEW terminal, set up frontend
cd .. && npm create vite@latest frontend -- --template react
cd frontend && npm install
npm install axios react-router-dom tailwindcss
npm run dev                           # Opens at http://localhost:3000

# 6. Run PostgreSQL with Docker (easiest way)
docker run --name hr-db \
  -e POSTGRES_USER=hruser \
  -e POSTGRES_PASSWORD=hrpass \
  -e POSTGRES_DB=hrdb \
  -p 5432:5432 -d postgres:15

# 7. Init Alembic migrations
cd backend
alembic init alembic
alembic revision --autogenerate -m "create initial tables"
alembic upgrade head                  # Creates tables in DB
08 — STEP BY STEP
Build Plan — Detailed Phases
1
Learn Before You Build
1–2 weeks
Before writing one line of project code, do these free courses. They'll save you weeks of confusion.

→
Python basics: functions, classes, imports (freeCodeCamp YouTube — "Python for Beginners")
→
FastAPI official tutorial: fastapi.tiangolo.com (do the whole "First Steps" section)
→
React basics: "React in 100 Seconds" on YouTube, then official react.dev tutorial
→
SQL basics: sqltutorial.org (SELECT, INSERT, UPDATE, DELETE — that's 80% of what you need)
→
Git: "Git in 15 Minutes" YouTube — learn add, commit, push, pull
2
Backend First, Always
Weeks 3–9
Build the backend completely and test it with Swagger UI (http://localhost:8000/docs) before touching React.

→
Create models → Run migration → Verify tables in PostgreSQL
→
Build one endpoint at a time — start with GET /employees/
→
Test EVERY endpoint in Swagger before moving on
→
Add auth last (it's easier to debug without auth first)
→
Use .env file for all secrets (never hardcode passwords in code)
3
Frontend & Connecting to Backend
Weeks 10–12
Once your API works perfectly, build the React UI to display and interact with the data.

→
Start with the Login page — it's the entry point to everything
→
Store JWT in localStorage and attach it to all API calls
→
Build a reusable API module (api/index.js) — don't repeat fetch calls everywhere
→
Build one page at a time: Employees → Leaves → Payroll → Dashboard
→
Use React Router for navigation between pages
4
Adding the AI Chatbot
Weeks 13–14
This is the magic layer. Claude AI reads your HR database and answers employee questions naturally.

→
Sign up at console.anthropic.com, get your API key
→
Add ANTHROPIC_API_KEY to your .env file
→
Build the /chat/message endpoint (fetch DB context → call Claude → return response)
→
Test chatbot: "How many leaves has Employee #1 taken?" — it should answer correctly
→
Build React ChatWidget.jsx — a floating chat bubble with message history
→
Add streaming for real-time typewriter effect responses
09 — TIPS
Common Beginner Mistakes to Avoid
✗
Don't skip tests.
Use FastAPI's Swagger UI (/docs) to test every endpoint before writing frontend code.
✗
Don't hardcode secrets.
Never put API keys or passwords in your code. Always use .env files.
✗
Don't build everything at once.
One feature at a time. Get it working, then move on.
✗
Don't ignore error messages.
Read them fully. Google the exact error. Stack Overflow is your best friend.
✗
Don't skip Git commits.
Commit after every working feature so you can always go back.
✓
Do use Docker for PostgreSQL
from day 1 — it saves you hours of local DB installation headaches.
✓
Do use FastAPI's built-in docs
— go to /docs as soon as the server starts. It's a free API testing tool.
Final Advice: You will get stuck. That's normal and it's how you learn. When stuck: (1) Read the error message carefully. (2) Google it. (3) Ask Claude. (4) Take a break and come back. Every senior engineer still googles things daily.
HR System Architecture Guide — Built for Nashrat
FastAPI · React · PostgreSQL · Claude AI · Docker