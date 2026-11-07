# * Main FastAPI Application Entrypoint
from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from app.storage.database import SessionLocal, JobRecord, init_db
from app.services.runner import run_research_job
from app.schemas.models import JobResponse, ResearchRequest

# todo Later: Break down routes into app/api/endpoints.py as the project grows
app = FastAPI(title="AI Research Team API")

# // Initialize the SQLite tables when the server boots
@app.on_event("startup")
def on_startup():
    init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/research", response_model=JobResponse)
def start_research(request: ResearchRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # * Insert the new job into the database
    new_job = JobRecord(status="PENDING")
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    
    # ? Handoff the heavy LangGraph execution to a separate non-blocking thread
    background_tasks.add_task(run_research_job, new_job.job_id, request.query)
    
    return JobResponse(
        job_id=new_job.job_id,
        status=new_job.status,
        message="Research task has been started in the background."
    )

@app.get("/api/jobs/{job_id}")
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    job = db.query(JobRecord).filter(JobRecord.job_id == job_id).first()
    if not job:
        # ! Return standard 404 to avoid exposing internal logic
        raise HTTPException(status_code=404, detail="Job not found")
        
    return {
        "job_id": job.job_id,
        "status": job.status,
        "result": job.result
    }