# * Service responsible for running LangGraph workflow safely in the background
from sqlalchemy.orm import Session
from app.storage.database import JobRecord, SessionLocal
from app.graph.workflow import create_research_graph
from langchain_core.messages import HumanMessage

def run_research_job(job_id: str, query: str):
    # ? Create a fresh DB session for this specific background thread
    db: Session = SessionLocal()
    job = db.query(JobRecord).filter(JobRecord.job_id == job_id).first()
    
    if not job:
        db.close()
        return
        
    job.status = "RUNNING"
    db.commit()

    try:
        # * Initialize and execute the multi-agent graph
        app = create_research_graph()
        initial_input = {
            "messages": [HumanMessage(content=query)],
            "retry_count": 0,
            "max_retries": 3,
            "review_feedback": None
        }
        
        result = app.invoke(initial_input)
        
        # // Extract the final AI output from the last message in the state
        final_report = result["messages"][-1].content
        
        job.result = final_report
        job.status = "COMPLETED"
    except Exception as e:
        # ! Critical to catch exceptions here, otherwise jobs remain stuck in RUNNING state forever
        job.status = "FAILED"
        job.result = str(e)
    finally:
        db.commit()
        db.close()