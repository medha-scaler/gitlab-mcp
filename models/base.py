# === models/base.py ===
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import sqlite3
import json

@dataclass
class BaseModel:
    """Base class for all models with common functionality"""
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
    
    def to_dict(self):
        """Convert model to dictionary for API responses"""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result
