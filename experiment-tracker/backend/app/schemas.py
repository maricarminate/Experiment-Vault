from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

class ExperimentStatus(str, Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class ExperimentCreate(BaseModel):
    name: str
    description: Optional[str] = None
    user: Optional[str] = None
    git_branch: Optional[str] = None
    git_commit: Optional[str] = None
    dataset_version: Optional[str] = None

class ExperimentUpdate(BaseModel):
    params: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, Any]] = None
    status: Optional[ExperimentStatus] = None

class ExperimentResponse(BaseModel):
    id: int
    name: str
    status: ExperimentStatus
    created_at: datetime
    updated_at: datetime
    user: Optional[str]
    git_branch: Optional[str]
    git_commit: Optional[str]
    dataset_version: Optional[str]
    description: Optional[str]
    params: Dict[str, Any]
    metrics: Dict[str, Any]
    artifacts: Dict[str, Any]
    
    class Config:
        from_attributes = True

class ExperimentCompare(BaseModel):
    experiment_ids: list[int]