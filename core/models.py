"""
GitLab MCP Simulation - Core Data Models
This module defines the basic data structures for our GitLab simulation.
"""

__all__ = [
    "User",
    "Project",
    "Issue",
    "Label",
    "IssueState",
    "ProjectVisibility"
]
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
import uuid

class IssueState(Enum):
    OPENED = "opened"
    CLOSED = "closed"

class ProjectVisibility(Enum):
    PRIVATE = "private"
    PUBLIC = "public"
    INTERNAL = "internal"

@dataclass
class User:
    """Represents a GitLab user/team member"""
    id: int
    username: str
    name: str
    email: str
    avatar_url: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Ensure we have a unique ID if not provided"""
        if not hasattr(self, '_id_set'):
            self.id = self.id or hash(self.username) % 10000

@dataclass
class Label:
    """Represents GitLab issue/MR labels"""
    id: int
    name: str
    color: str  # Hex color code
    description: Optional[str] = None
    
    def __post_init__(self):
        if not self.color.startswith('#'):
            self.color = f"#{self.color}"

@dataclass
class Project:
    """Represents a GitLab project/repository"""
    id: int
    name: str
    description: str
    visibility: ProjectVisibility = ProjectVisibility.PRIVATE
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    owner_id: Optional[int] = None
    
    # Collections
    issues: List['Issue'] = field(default_factory=list)
    members: List[User] = field(default_factory=list)
    labels: List[Label] = field(default_factory=list)

@dataclass
class Issue:
    """Represents a GitLab issue"""
    id: int
    title: str
    description: str
    project_id: int
    author_id: int
    state: IssueState = IssueState.OPENED
    assignee_id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    closed_at: Optional[datetime] = None
    
    # Collections
    labels: List[str] = field(default_factory=list)  # Label names
    comments: List['Comment'] = field(default_factory=list)

@dataclass
class Comment:
    """Represents a comment on an issue or merge request"""
    id: int
    body: str
    author_id: int
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

# Example usage and testing
if __name__ == "__main__":
    # Create some sample data to test our models
    
    # Create users
    alice = User(id=1, username="alice", name="Alice Smith", email="alice@example.com")
    bob = User(id=2, username="bob", name="Bob Johnson", email="bob@example.com")
    
    # Create labels
    bug_label = Label(id=1, name="bug", color="FF0000", description="Something isn't working")
    feature_label = Label(id=2, name="enhancement", color="00FF00", description="New feature request")
    
    # Create a project
    project = Project(
        id=1,
        name="awesome-app",
        description="An awesome application for demonstration",
        owner_id=alice.id,
        members=[alice, bob],
        labels=[bug_label, feature_label]
    )
    
    # Create an issue
    issue = Issue(
        id=1,
        title="Fix login bug",
        description="Users cannot log in with special characters in password",
        project_id=project.id,
        author_id=alice.id,
        assignee_id=bob.id,
        labels=["bug"]
    )
    
    # Add issue to project
    project.issues.append(issue)
    
    print("✅ Core data models created successfully!")
    print(f"Project: {project.name} with {len(project.issues)} issues")
    print(f"Issue: {issue.title} - {issue.state.value}")
    print(f"Assigned to: {bob.name}")