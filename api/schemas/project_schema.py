# === api/schemas/project_schemas.py ===
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str
    description: str
    visibility: str = "private"  # private, public, internal

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    visibility: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    visibility: str
    owner_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProjectWithStats(ProjectResponse):
    """Project with additional statistics"""
    issues_count: int
    open_issues_count: int
    members_count: int
