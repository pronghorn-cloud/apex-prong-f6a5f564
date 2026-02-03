from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from backend.src.database import engine, Base, get_db
from backend.src.models import policy as models
from backend.src.api import policies, users, auth_api, workflows, notifications, reports

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_api.router)
app.include_router(policies.router)
app.include_router(users.router)
app.include_router(workflows.router)
app.include_router(notifications.router)
app.include_router(reports.router)


app.include_router(auth_api.router)
app.include_router(policies.router)
app.include_router(users.router)
app.include_router(workflows.router)
app.include_router(notifications.router)


app.include_router(auth_api.router)
app.include_router(policies.router)
app.include_router(users.router)
app.include_router(workflows.router)


app.include_router(auth_api.router)
app.include_router(policies.router)
app.include_router(users.router)


app.include_router(policies.router)
app.include_router(users.router)

app = FastAPI()

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
