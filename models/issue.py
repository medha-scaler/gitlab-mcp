# === models/issue.py ===
from dataclasses import dataclass, field
from models.base import BaseModel
from enum import Enum
from typing import List

class IssueState(Enum):
    OPENED = "opened"
    CLOSED = "closed"

@dataclass
class Issue(BaseModel):
    title: str = ""
    description: str = ""
    project_id: Optional[int] = None
    author_id: Optional[int] = None
    assignee_id: Optional[int] = None
    state: IssueState = IssueState.OPENED
    labels: List[str] = field(default_factory=list)