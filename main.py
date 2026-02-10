from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow your frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace * with your frontend domain
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ERP System Online"}

# This is the endpoint your Dashboard is calling!
@app.get("/dashboard/summary")
def get_dashboard_summary():
    # TODO: In the future, we will fetch this data from the PostgreSQL database.
    # For now, we return the "Real" data structure so the Frontend works.
    return {
        "stats": [
            { "label": "Health & Wellness", "value": "$450", "sub": "Remaining", "icon": "favorite", "color": "bg-rose-50 text-rose-600", "border": "border-rose-100 border-l-4 border-l-rose-500" },
            { "label": "Boots Allowance", "value": "$120", "sub": "Remaining", "icon": "snowshoeing", "color": "bg-amber-50 text-amber-600", "border": "border-amber-100 border-l-4 border-l-amber-500" },
            { "label": "Tools Allowance", "value": "$350", "sub": "Remaining", "icon": "build", "color": "bg-blue-50 text-blue-600", "border": "border-blue-100 border-l-4 border-l-blue-500" },
            { "label": "Safety Rewards", "value": "1,250", "sub": "Points", "icon": "emoji_events", "color": "bg-emerald-50 text-emerald-600", "border": "border-emerald-100 border-l-4 border-l-emerald-500" },
            { "label": "CyberAware", "value": "750", "sub": "Points", "icon": "security", "color": "bg-purple-50 text-purple-600", "border": "border-purple-100 border-l-4 border-l-purple-500" },
        ],
        "activity": [
            { "id": 1, "user": "Backend", "color": "bg-blue-100 text-blue-700", "text": "Connected to API", "sub": "System • Just now" },
            { "id": 2, "user": "JD", "color": "bg-green-100 text-green-700", "text": "Closed Hazard #HAZ-042", "sub": "Wiring Issue • 4 hours ago" },
            { "id": 3, "user": "MR", "color": "bg-orange-100 text-orange-700", "text": "Reported Near Miss", "sub": "Loading Dock • Yesterday" },
        ],
        "tasks": [
            { "title": "Approve Risk Assessment", "due": "Today", "priority": "High", "color": "text-red-600 bg-red-50" },
            { "title": "Weekly Safety Inspection", "due": "Tomorrow", "priority": "Medium", "color": "text-orange-600 bg-orange-50" },
            { "title": "Review Incident #INC-001", "due": "Feb 12", "priority": "Low", "color": "text-blue-600 bg-blue-50" },
        ],
        "learning": [
            { "title": "H&S Crash Course", "progress": 100, "status": "Completed", "date": "Jan 15" },
            { "title": "Fire Safety Basics", "progress": 75, "status": "In Progress", "date": "Due Feb 20" },
        ],
        "quizzes": [
            { "title": "WHMIS 2015 Refresher", "score": "95%", "status": "Pass", "color": "text-green-600 bg-green-50" },
            { "title": "Ladder Safety Quiz", "score": "80%", "status": "Pass", "color": "text-green-600 bg-green-50" },
        ],
        "certs": [
            { "title": "Fall Protection L2", "date": "Exp: 2026-01-15", "status": "Expired", "color": "bg-red-50 text-red-700 border-red-100", "icon": "warning" },
            { "title": "Forklift Operator", "date": "Exp: 2027-06-20", "status": "Active", "color": "bg-green-50 text-green-700 border-green-100", "icon": "check_circle" },
        ]
    }