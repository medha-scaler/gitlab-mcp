# === api/schemas/issue_schema.py ===
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class IssueCreate(BaseModel):
    title: str
    description: str
    project_id: int
    assignee_id: Optional[int] = None
    state: str = "opened"
    labels: Optional[List[str]] = []

class IssueUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    state: Optional[str] = None
    labels: Optional[List[str]] = None

class IssueResponse(BaseModel):
    id: int
    title: str
    description: str
    project_id: int
    author_id: Optional[int] = None
    assignee_id: Optional[int] = None
    state: str
    labels: List[str] = []
    created_at: datetime
    updated_at: datetime
    
    # Related data
    project_name: Optional[str] = None
    author_name: Optional[str] = None
    assignee_name: Optional[str] = None

    class Config:
        from_attributes = True