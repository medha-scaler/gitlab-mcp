# === api/routes/project.py ===
from fastapi import APIRouter, HTTPException
from typing import List, Optional
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from database.connection import DatabaseManager
from api.schemas.project_schema import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectWithStats

router = APIRouter()

@router.get("/projects", response_model=List[ProjectWithStats])
async def get_projects(limit: int = 100, offset: int = 0):
    """Get all projects with statistics"""
    query = """
        SELECT p.*, u.name as owner_name,
               COUNT(DISTINCT i.id) as issues_count,
               COUNT(DISTINCT CASE WHEN i.state = 'opened' THEN i.id END) as open_issues_count
        FROM projects p
        LEFT JOIN users u ON p.owner_id = u.id
        LEFT JOIN issues i ON p.id = i.project_id
        GROUP BY p.id, p.name, p.description, p.visibility, p.owner_id, p.created_at, p.updated_at, u.name
        ORDER BY p.created_at DESC
        LIMIT ? OFFSET ?
    """
    
    projects = DatabaseManager.execute_query(query, (limit, offset))
    
    # Add members_count (simplified - in real app would be from project_members table)
    for project in projects:
        project['members_count'] = 1  # Owner only for now
    
    return projects

@router.get("/projects/{project_id}", response_model=ProjectWithStats)
async def get_project(project_id: int):
    """Get project by ID with statistics"""
    query = """
        SELECT p.*, u.name as owner_name,
               COUNT(DISTINCT i.id) as issues_count,
               COUNT(DISTINCT CASE WHEN i.state = 'opened' THEN i.id END) as open_issues_count
        FROM projects p
        LEFT JOIN users u ON p.owner_id = u.id
        LEFT JOIN issues i ON p.id = i.project_id
        WHERE p.id = ?
        GROUP BY p.id, p.name, p.description, p.visibility, p.owner_id, p.created_at, p.updated_at, u.name
    """
    
    projects = DatabaseManager.execute_query(query, (project_id,))
    
    if not projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project = projects[0]
    project['members_count'] = 1  # Simplified
    return project

@router.post("/projects", response_model=ProjectResponse)
async def create_project(project: ProjectCreate, owner_id: Optional[int] = None):
    """Create a new project"""
    query = """
        INSERT INTO projects (name, description, visibility, owner_id) 
        VALUES (?, ?, ?, ?)
    """
    
    try:
        project_id = DatabaseManager.execute_insert(
            query, 
            (project.name, project.description, project.visibility, owner_id)
        )
        
        # Return the created project
        return await get_project(project_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create project: {str(e)}")

@router.patch("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, project_update: ProjectUpdate):
    """Update an existing project"""
    # Check if project exists
    existing = DatabaseManager.execute_query("SELECT * FROM projects WHERE id = ?", (project_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Build update query dynamically
    update_fields = []
    params = []
    
    if project_update.name is not None:
        update_fields.append("name = ?")
        params.append(project_update.name)
    
    if project_update.description is not None:
        update_fields.append("description = ?")
        params.append(project_update.description)
    
    if project_update.visibility is not None:
        update_fields.append("visibility = ?")
        params.append(project_update.visibility)
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    update_fields.append("updated_at = CURRENT_TIMESTAMP")
    params.append(project_id)
    
    query = f"UPDATE projects SET {', '.join(update_fields)} WHERE id = ?"
    
    DatabaseManager.execute_update(query, params)
    
    return await get_project(project_id)

@router.get("/projects/{project_id}/issues")
async def get_project_issues(project_id: int, state: Optional[str] = None):
    """Get all issues for a project"""
    # Check if project exists
    existing = DatabaseManager.execute_query("SELECT * FROM projects WHERE id = ?", (project_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Project not found")
    
    base_query = """
        SELECT i.*, a.name as author_name, as_u.name as assignee_name
        FROM issues i
        LEFT JOIN users a ON i.author_id = a.id  
        LEFT JOIN users as_u ON i.assignee_id = as_u.id
        WHERE i.project_id = ?
    """
    
    params = [project_id]
    
    if state:
        base_query += " AND i.state = ?"
        params.append(state)
    
    base_query += " ORDER BY i.created_at DESC"
    
    issues = DatabaseManager.execute_query(base_query, params)
    
    # Parse labels JSON
    for issue in issues:
        if issue['labels']:
            import json
            issue['labels'] = json.loads(issue['labels'])
        else:
            issue['labels'] = []
    
    return issues