from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
import auth
from database import engine, get_db

# --- DATABASE STARTUP ---
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://staging.158.69.63.190.sslip.io", 
        "https://app.checkifsafe.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    email: str
    password: str

@app.get("/")
def read_root():
    return {"status": "ERP System Online"}

@app.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user or not auth.verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    access_token = auth.create_access_token(data={"sub": user.email, "tenant_id": user.tenant_id, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer", "user": {"full_name": user.full_name, "email": user.email, "tenant_id": user.tenant_id}}

@app.get("/dashboard/summary")
def get_dashboard_summary():
    return {
        "stats": [
            {"label": "Health & Wellness", "value": "$450", "sub": "Remaining", "icon": "favorite", "color": "bg-rose-50 text-rose-600", "border": "border-rose-100 border-l-4 border-l-rose-500"},
            {"label": "Boots Allowance", "value": "$120", "sub": "Remaining", "icon": "snowshoeing", "color": "bg-amber-50 text-amber-600", "border": "border-amber-100 border-l-4 border-amber-500"},
            {"label": "Tools Allowance", "value": "$350", "sub": "Remaining", "icon": "handyman", "color": "bg-blue-50 text-blue-600", "border": "border-blue-100 border-l-4 border-blue-500"},
            {"label": "Safety Rewards", "value": "1,250", "sub": "Points", "icon": "emoji_events", "color": "bg-emerald-50 text-emerald-600", "border": "border-emerald-100 border-l-4 border-emerald-500"},
            {"label": "CyberAware", "value": "750", "sub": "Points", "icon": "security", "color": "bg-purple-50 text-purple-600", "border": "border-purple-100 border-l-4 border-purple-500"},
        ],
        "activity": [
            # UPDATED: Changed keys to 'title' and 'description' and matched Prod content
            {
                "user": "John Doe", 
                "initials": "JD", 
                "title": "Submitted Warehouse Audit", # Was 'action'
                "description": "Warehouse B",         # Was 'target'
                "time": "2 hours ago", 
                "color": "bg-blue-100 text-blue-600"
            },
            {
                "user": "Sarah Moss", 
                "initials": "SM", 
                "title": "Closed Hazard #HAZ-042",    # Was 'action'
                "description": "Wiring Issue",        # Was 'target'
                "time": "4 hours ago", 
                "color": "bg-green-100 text-green-600"
            },
            {
                "user": "Mike Ross",
                "initials": "MR",
                "title": "Reported Near Miss",
                "description": "Loading Dock",
                "time": "Yesterday",
                "color": "bg-orange-100 text-orange-600"
            }
        ],
        "tasks": [
            {"title": "Approve Risk Assessment", "due": "Today", "priority": "High", "type": "Review"},
            {"title": "Weekly Safety Inspection", "due": "Tomorrow", "priority": "Medium", "type": "Inspection"},
            {"title": "Update Certification", "due": "Feb 15", "priority": "Medium", "type": "Compliance"}
        ],
        "learning": [
            {"title": "H&S Crash Course", "progress": 100, "due": "Jan 15", "status": "Completed"},
            {"title": "Fire Safety Basics", "progress": 75, "due": "Due Feb 20", "status": "In Progress"},
            {"title": "Ergonomics 101", "progress": 0, "due": "Due Mar 01", "status": "Not Started"}
        ],
        "quizzes": [
             {"title": "WHMIS 2015 Refresher", "score": "95%", "status": "Pass"},
             {"title": "Ladder Safety Quiz", "score": "80%", "status": "Pass"},
             {"title": "PPE Standards Check", "score": "-", "status": "Pending"}
        ],
        "certs": [
            {"title": "Fall Protection L2", "expiry": "Exp: 2026-01-15", "status": "Expired", "status_color": "bg-red-100 text-red-700"},
            {"title": "First Aid Level C", "expiry": "Exp: 2026-03-01", "status": "Expiring Soon", "status_color": "bg-orange-100 text-orange-700"},
            {"title": "Forklift Operator", "expiry": "Active", "status": "Active", "status_color": "bg-green-100 text-green-700"}
        ]
    }

# --- SIDEBAR MODULE ENDPOINTS ---

@app.get("/tasks")
def get_tasks():
    return [{"id": 1, "title": "Approve Risk Assessment", "due": "Today", "priority": "High", "status": "Pending"}]

@app.get("/learning")
def get_learning():
    return {"courses": [{"id": 101, "title": "H&S Crash Course", "progress": 100, "status": "Completed"}]}

@app.get("/health-safety/incidents")
def get_incidents():
    return [{"id": "INC-001", "type": "Near Miss", "location": "Warehouse B", "status": "Open"}]

@app.get("/documents")
def get_documents():
    return [{"id": 1, "name": "Employee Handbook.pdf", "category": "Policy"}]