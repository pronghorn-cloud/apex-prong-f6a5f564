from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend.src.database import engine, Base, get_db
from backend.src.models import policy as models
from backend.src.api import policies, users, auth_api, workflows, notifications, reports

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://dev-apex-prong-f6a5f564-service-jwr1.onrender.com"], # Adjust as needed for your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_api.router)
app.include_router(policies.router)
app.include_router(users.router)
app.include_router(workflows.router)
app.include_router(notifications.router)
app.include_router(reports.router)


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "detail": str(e)}

# Serve static files for the frontend
app.mount("/", StaticFiles(directory="./frontend/dist", html=True), name="frontend")

app.include_router(policies.router)


app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Power Policy Backend is running!"}

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "detail": str(e)}


@app.get("/")
async def read_root():
    return {"message": "Power Policy Backend is running!"}
