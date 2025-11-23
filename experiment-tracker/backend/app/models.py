from sqlalchemy import Column, Integer, String, DateTime, JSON, Float, Enum as SQLEnum
from datetime import datetime
import enum
from app.db import Base

class ExperimentStatus(str, enum.Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class Experiment(Base):
    __tablename__ = "experiments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    status = Column(SQLEnum(ExperimentStatus), default=ExperimentStatus.RUNNING)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Metadados
    user = Column(String, nullable=True)
    git_branch = Column(String, nullable=True)
    git_commit = Column(String, nullable=True)
    dataset_version = Column(String, nullable=True)
    description = Column(String, nullable=True)
    
    # Dados armazenados como JSON
    params = Column(JSON, default={})
    metrics = Column(JSON, default={})
    artifacts = Column(JSON, default={})  # {"model": "path/to/model.pkl", ...}
    
    class Config:
        from_attributes = True