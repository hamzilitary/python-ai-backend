from pydantic import BaseModel
from datetime import datetime

class CreateRunRequest(BaseModel):
    goal: str
    context: str | None = None

class GetRunsRequest(BaseModel):
    goal: str
    context: str

class GetRunRequest(BaseModel):
    run_id: str

class UpdateStatus(BaseModel):
    status: str

class AgentRun(BaseModel):
    id: int
    goal: str 
    context: str | None = None
    status: str
    created_at: datetime
    response: str | None = None
    model: str | None = None
    error: str | None = None
    completed_at: datetime | None = None
    latency_ms: int | None = None
    user_id: int | None = None
    model_id: int | None = None
