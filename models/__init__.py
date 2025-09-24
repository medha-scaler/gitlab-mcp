# === Complete models/__init__.py ===
from .base import BaseModel
from .user import User
from .project import Project, ProjectVisibility
from .issue import Issue, IssueState

__all__ = [
    "BaseModel",
    "User", 
    "Project", "ProjectVisibility",
    "Issue", "IssueState"
]
