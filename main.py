from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
import auth
from database import engine, get_db

# --- DATABASE STARTUP ---
# Creates the tables in Postgres if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- SECURITY (CORS) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://staging.158.69.63.190.sslip.io", 
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SCHEMAS ---
class LoginRequest(BaseModel):
    email: str
    password: str

# --- ROUTES ---

@app.get("/")
def read_root():
    return {"status": "ERP System Online"}

@app.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    
    if not user or not auth.verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = auth.create_access_token(data={
        "sub": user.email, 
        "tenant_id": user.tenant_id,
        "role": user.role
    })

    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {
            "full_name": user.full_name,
            "email": user.email,
            "tenant_id": user.tenant_id
        }
    }

@app.get("/dashboard/summary")
def get_dashboard_summary():
    # This is the "Mock Data" that makes your frontend dashboard look pretty
    return {
        "stats": [
            {"label": "Health & Wellness", "value": "$450", "sub": "Remaining", "icon": "favorite", "color": "bg-rose-50 text-rose-600", "border": "border-rose-100 border-l-4 border-l-rose-500"},
            {"label": "Boots Allowance", "value": "$120", "sub": "Remaining", "icon": "snowshoeing", "color": "bg-amber-50 text-amber-600", "border": "border-amber-100 border-l-4 border-amber-500"},
            {"label": "Tools Allowance", "value": "$350", "sub": "Remaining", "icon": "handyman", "color": "bg-blue-50 text-blue-600", "border": "border-blue-100 border-l-4 border-blue-500"},
            {"label": "Safety Rewards", "value": "1,250", "sub": "Points", "icon": "emoji_events", "color": "bg-emerald-50 text-emerald-600", "border": "border-emerald-100 border-l-4 border-emerald-500"},
            {"label": "CyberAware", "value": "750", "sub": "Points", "icon": "security", "color": "bg-purple-50 text-purple-600", "border": "border-purple-100 border-l-4 border-purple-500"},
        ],
        "recent_activity": [
            {"user": "Admin", "action": "Logged in", "target": "System", "time": "Just now", "initials": "AD", "color": "bg-blue-100 text-blue-600"},
            {"user": "JD", "action": "Closed Hazard #HAZ-042", "target": "Wiring Issue", "time": "4 hours ago", "initials": "JD", "color": "bg-green-100 text-green-600"},
        ]
    }