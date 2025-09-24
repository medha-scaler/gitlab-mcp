# === api/schemas/user_schema.py ===
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    name: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    email: str
    avatar_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True