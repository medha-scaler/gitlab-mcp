# === models/user.py ===
from dataclasses import dataclass
from models.base import BaseModel

@dataclass
class User(BaseModel):
    username: str = ""
    name: str = ""
    email: str = ""
    avatar_url: Optional[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        if not self.avatar_url:
            self.avatar_url = f"https://avatar.example.com/{self.username}.png"
