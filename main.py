from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow your frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace * with your frontend domain
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ERP System Online"}

@app.get("/api/dashboard-stats")
def get_stats():
    # This mocks data. Later, you fetch this from the DB.
    return {
        "incidents": 3,
        "tasks_pending": 12,
        "budget_status": "On Track"
    }