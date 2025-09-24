# === api/routes/user.py ===
from fastapi import APIRouter, HTTPException
from typing import List, Optional
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from database.connection import DatabaseManager
from api.schemas.user_schema import UserCreate, UserResponse

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
async def get_users(limit: int = 100, offset: int = 0):
    """Get all users with pagination"""
    query = "SELECT * FROM users ORDER BY created_at DESC LIMIT ? OFFSET ?"
    users = DatabaseManager.execute_query(query, (limit, offset))
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Get user by ID"""
    query = "SELECT * FROM users WHERE id = ?"
    users = DatabaseManager.execute_query(query, (user_id,))
    
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    
    return users[0]

@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    """Create a new user"""
    query = """
        INSERT INTO users (username, name, email, avatar_url) 
        VALUES (?, ?, ?, ?)
    """
    
    avatar_url = f"https://avatar.example.com/{user.username}.png"
    
    try:
        user_id = DatabaseManager.execute_insert(
            query, 
            (user.username, user.name, user.email, avatar_url)
        )
        
        # Return the created user
        return await get_user(user_id)
        
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(status_code=400, detail="Username or email already exists")
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")

@router.get("/users/{user_id}/issues")
async def get_user_issues(user_id: int, state: Optional[str] = None):
    """Get all issues assigned to or created by a user"""
    base_query = """
        SELECT i.*, p.name as project_name, 
               a.name as author_name, as_u.name as assignee_name
        FROM issues i
        LEFT JOIN projects p ON i.project_id = p.id
        LEFT JOIN users a ON i.author_id = a.id  
        LEFT JOIN users as_u ON i.assignee_id = as_u.id
        WHERE (i.assignee_id = ? OR i.author_id = ?)
    """
    
    params = [user_id, user_id]
    
    if state:
        base_query += " AND i.state = ?"
        params.append(state)
    
    base_query += " ORDER BY i.updated_at DESC"
    
    issues = DatabaseManager.execute_query(base_query, params)
    
    # Parse labels JSON
    for issue in issues:
        if issue['labels']:
            import json
            issue['labels'] = json.loads(issue['labels'])
        else:
            issue['labels'] = []
    
    return issues