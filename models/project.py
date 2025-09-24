# === models/project.py ===
from dataclasses import dataclass
from models.base import BaseModel
from enum import Enum

class ProjectVisibility(Enum):
    PRIVATE = "private"
    PUBLIC = "public"
    INTERNAL = "internal"

@dataclass
class Project(BaseModel):
    name: str = ""
    description: str = ""
    visibility: ProjectVisibility = ProjectVisibility.PRIVATE
    owner_id: Optional[int] = None