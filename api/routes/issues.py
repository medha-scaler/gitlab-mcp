from fastapi import APIRouter, HTTPException
from typing import List, Optional
import json
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from database.connection import DatabaseManager
from api.schemas.issue_schema import IssueCreate, IssueUpdate, IssueResponse

router = APIRouter()

@router.get("/issues", response_model=List[IssueResponse])
async def get_issues(
    state: Optional[str] = None,
    assignee_id: Optional[int] = None,
    project_id: Optional[int] = None,
    limit: int = 100,
    offset: int = 0
):
    """Get all issues with filtering options"""
    base_query = """
        SELECT i.*, p.name as project_name, 
               a.name as author_name, as_u.name as assignee_name
        FROM issues i
        LEFT JOIN projects p ON i.project_id = p.id
        LEFT JOIN users a ON i.author_id = a.id  
        LEFT JOIN users as_u ON i.assignee_id = as_u.id
        WHERE 1=1
    """
    
    params = []
    
    if state:
        base_query += " AND i.state = ?"
        params.append(state)
    
    if assignee_id:
        base_query += " AND i.assignee_id = ?"
        params.append(assignee_id)
    
    if project_id:
        base_query += " AND i.project_id = ?"
        params.append(project_id)
    
    base_query += " ORDER BY i.updated_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    issues = DatabaseManager.execute_query(base_query, params)
    
    # Parse labels JSON
    for issue in issues:
        if issue['labels']:
            issue['labels'] = json.loads(issue['labels'])
        else:
            issue['labels'] = []
    
    return issues

@router.get("/issues/{issue_id}", response_model=IssueResponse)
async def get_issue(issue_id: int):
    """Get issue by ID"""
    query = """
        SELECT i.*, p.name as project_name, 
               a.name as author_name, as_u.name as assignee_name
        FROM issues i
        LEFT JOIN projects p ON i.project_id = p.id
        LEFT JOIN users a ON i.author_id = a.id  
        LEFT JOIN users as_u ON i.assignee_id = as_u.id
        WHERE i.id = ?
    """
    
    issues = DatabaseManager.execute_query(query, (issue_id,))
    
    if not issues:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    issue = issues[0]
    
    # Parse labels JSON
    if issue['labels']:
        issue['labels'] = json.loads(issue['labels'])
    else:
        issue['labels'] = []
    
    return issue

@router.post("/issues", response_model=IssueResponse)
async def create_issue(issue: IssueCreate, author_id: Optional[int] = None):
    """Create a new issue"""
    # Validate project exists
    project_check = DatabaseManager.execute_query(
        "SELECT id FROM projects WHERE id = ?", 
        (issue.project_id,)
    )
    if not project_check:
        raise HTTPException(status_code=400, detail="Project not found")
    
    # Validate assignee exists if provided
    if issue.assignee_id:
        assignee_check = DatabaseManager.execute_query(
            "SELECT id FROM users WHERE id = ?", 
            (issue.assignee_id,)
        )
        if not assignee_check:
            raise HTTPException(status_code=400, detail="Assignee not found")
    
    labels_json = json.dumps(issue.labels) if issue.labels else json.dumps([])
    
    query = """
        INSERT INTO issues (title, description, project_id, author_id, assignee_id, state, labels) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    
    try:
        issue_id = DatabaseManager.execute_insert(
            query, 
            (issue.title, issue.description, issue.project_id, 
             author_id, issue.assignee_id, issue.state, labels_json)
        )
        # Return the created issue
        return await get_issue(issue_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create issue: {str(e)}")

@router.patch("/issues/{issue_id}", response_model=IssueResponse)
async def update_issue(issue_id: int, issue_update: IssueUpdate):
    """Update an existing issue"""
    # Check if issue exists
    existing = DatabaseManager.execute_query("SELECT * FROM issues WHERE id = ?", (issue_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    # Build update query dynamically
    update_fields = []
    params = []
    
    if issue_update.title is not None:
        update_fields.append("title = ?")
        params.append(issue_update.title)
    
    if issue_update.description is not None:
        update_fields.append("description = ?")
        params.append(issue_update.description)
    
    if issue_update.assignee_id is not None:
        # Validate assignee exists
        assignee_check = DatabaseManager.execute_query(
            "SELECT id FROM users WHERE id = ?", 
            (issue_update.assignee_id,)
        )
        if not assignee_check:
            raise HTTPException(status_code=400, detail="Assignee not found")
        update_fields.append("assignee_id = ?")
        params.append(issue_update.assignee_id)
    
    if issue_update.state is not None:
        update_fields.append("state = ?")
        params.append(issue_update.state)
    
    if issue_update.labels is not None:
        update_fields.append("labels = ?")
        params.append(json.dumps(issue_update.labels))
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    update_fields.append("updated_at = CURRENT_TIMESTAMP")
    params.append(issue_id)
    
    query = f"UPDATE issues SET {', '.join(update_fields)} WHERE id = ?"
    
    DatabaseManager.execute_update(query, params)
    
    return await get_issue(issue_id)

@router.delete("/issues/{issue_id}")
async def delete_issue(issue_id: int):
    """Delete an issue"""
    # Check if issue exists
    existing = DatabaseManager.execute_query("SELECT * FROM issues WHERE id = ?", (issue_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    DatabaseManager.execute_update("DELETE FROM issues WHERE id = ?", (issue_id,))
    
    return {"message": f"Issue {issue_id} deleted successfully"}

# Admin endpoints for bulk operations (AI training tasks)
@router.get("/admin/stats")
async def get_system_stats():
    """Get comprehensive system statistics for AI analysis"""
    # Basic counts
    user_count = DatabaseManager.execute_query("SELECT COUNT(*) as count FROM users")[0]['count']
    project_count = DatabaseManager.execute_query("SELECT COUNT(*) as count FROM projects")[0]['count']
    total_issues = DatabaseManager.execute_query("SELECT COUNT(*) as count FROM issues")[0]['count']
    open_issues = DatabaseManager.execute_query("SELECT COUNT(*) as count FROM issues WHERE state = 'opened'")[0]['count']
    
    # Workload distribution
    workload_query = """
        SELECT u.id, u.username, u.name,
               COUNT(i.id) as assigned_issues,
               COUNT(CASE WHEN i.state = 'opened' THEN 1 END) as open_assigned
        FROM users u
        LEFT JOIN issues i ON u.id = i.assignee_id
        GROUP BY u.id, u.username, u.name
        ORDER BY assigned_issues DESC
    """
    workload = DatabaseManager.execute_query(workload_query)
    
    # Project health
    project_health_query = """
        SELECT p.id, p.name,
               COUNT(i.id) as total_issues,
               COUNT(CASE WHEN i.state = 'opened' THEN 1 END) as open_issues
        FROM projects p
        LEFT JOIN issues i ON p.id = i.project_id
        GROUP BY p.id, p.name
    """
    project_health = DatabaseManager.execute_query(project_health_query)
    
    # Label distribution (for AI training insights)
    label_stats = {}
    all_issues = DatabaseManager.execute_query("SELECT labels FROM issues WHERE labels IS NOT NULL")
    for issue in all_issues:
        if issue['labels']:
            labels = json.loads(issue['labels'])
            for label in labels:
                label_stats[label] = label_stats.get(label, 0) + 1
    
    return {
        "users": user_count,
        "projects": project_count,
        "issues": {
            "total": total_issues,
            "open": open_issues,
            "closed": total_issues - open_issues
        },
        "workload_distribution": workload,
        "project_health": project_health,
        "label_distribution": label_stats,
        "ai_insights": {
            "avg_issues_per_user": total_issues / max(user_count, 1),
            "completion_rate": ((total_issues - open_issues) / max(total_issues, 1)) * 100,
            "most_common_labels": sorted(label_stats.items(), key=lambda x: x[1], reverse=True)[:5]
        }
    }

@router.post("/admin/bulk-reassign")
async def bulk_reassign_issues(from_user_id: int, to_user_id: int, limit: int = 5):
    """Bulk reassign issues from one user to another (AI training task)"""
    # Validate users exist
    from_user = DatabaseManager.execute_query("SELECT * FROM users WHERE id = ?", (from_user_id,))
    to_user = DatabaseManager.execute_query("SELECT * FROM users WHERE id = ?", (to_user_id,))
    
    if not from_user:
        raise HTTPException(status_code=404, detail="From user not found")
    if not to_user:
        raise HTTPException(status_code=404, detail="To user not found")
    
    # Get open issues assigned to from_user
    issues = DatabaseManager.execute_query(
        "SELECT id FROM issues WHERE assignee_id = ? AND state = 'opened' LIMIT ?",
        (from_user_id, limit)
    )
    
    if not issues:
        return {"message": "No open issues found for reassignment", "reassigned_count": 0}
    
    # Reassign issues
    issue_ids = [issue['id'] for issue in issues]
    for issue_id in issue_ids:
        DatabaseManager.execute_update(
            "UPDATE issues SET assignee_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (to_user_id, issue_id)
        )
    
    return {
        "message": f"Reassigned {len(issue_ids)} issues from {from_user[0]['name']} to {to_user[0]['name']}",
        "reassigned_count": len(issue_ids),
        "issue_ids": issue_ids
    }