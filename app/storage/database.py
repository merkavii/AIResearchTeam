# * Setup database connection and ORM models using SQLAlchemy
from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import uuid
from app.core.config import settings

# ? check_same_thread=False is required in SQLite when connections are shared across BackgroundTasks threads
engine = create_engine(
    settings.database_url, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class JobRecord(Base):
    __tablename__ = "jobs"
    
    job_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    status = Column(String, default="PENDING")  # // PENDING, RUNNING, COMPLETED, FAILED
    result = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# ! Must be called on application startup to ensure tables exist
def init_db():
    Base.metadata.create_all(bind=engine)