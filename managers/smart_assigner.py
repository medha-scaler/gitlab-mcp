"""
Smart Assignment Logic for GitLab MCP Simulator
This shows how we can add intelligent assignment and labeling logic
"""

from core.models import User, Project, Issue, Label, IssueState
from typing import List, Optional
import random
from dataclasses import dataclass

@dataclass 
class UserSkills:
    """Track what each user is good at"""
    user_id: int
    skills: List[str]  # e.g., ["frontend", "backend", "mobile", "testing"]
    current_workload: int = 0  # How many issues assigned
    max_capacity: int = 5      # Max issues they can handle

class SmartAssigner:
    """Handles intelligent assignment of issues to team members"""
    
    def __init__(self):
        self.user_skills = {}  # user_id -> UserSkills
        
    def add_user_skills(self, user_id: int, skills: List[str], max_capacity: int = 5):
        """Define what each user is good at"""
        self.user_skills[user_id] = UserSkills(
            user_id=user_id,
            skills=skills,
            max_capacity=max_capacity
        )
    
    def auto_assign_labels(self, issue_title: str, issue_description: str) -> List[str]:
        """Automatically suggest labels based on issue content"""
        labels = []
        content = (issue_title + " " + issue_description).lower()
        
        # Bug detection keywords
        bug_keywords = ["crash", "error", "bug", "broken", "fails", "not working", "issue"]
        if any(keyword in content for keyword in bug_keywords):
            labels.append("bug")
            
        # Priority detection
        urgent_keywords = ["urgent", "critical", "asap", "immediately", "crash", "down"]
        if any(keyword in content for keyword in urgent_keywords):
            labels.append("urgent")
            
        # Feature detection
        feature_keywords = ["add", "new", "feature", "implement", "support", "create"]
        if any(keyword in content for keyword in feature_keywords):
            labels.append("enhancement")
            
        # Technology detection
        if any(tech in content for tech in ["mobile", "android", "ios", "app"]):
            labels.append("mobile")
        if any(tech in content for tech in ["frontend", "ui", "interface", "design"]):
            labels.append("frontend")
        if any(tech in content for tech in ["backend", "api", "server", "database"]):
            labels.append("backend")
            
        return labels if labels else ["general"]  # Default label
    
    def find_best_assignee(self, issue: Issue, project: Project) -> Optional[int]:
        """Find the best person to assign this issue to"""
        
        # Get issue labels to understand what skills are needed
        required_skills = self._get_required_skills(issue.labels)
        
        # Score each team member
        candidates = []
        for member in project.members:
            if member.id not in self.user_skills:
                continue  # Skip users without defined skills
                
            user_skills = self.user_skills[member.id]
            
            # Skip if user is at capacity
            if user_skills.current_workload >= user_skills.max_capacity:
                continue
                
            # Calculate skill match score
            skill_score = self._calculate_skill_match(user_skills.skills, required_skills)
            
            # Calculate workload score (prefer less busy people)
            workload_score = (user_skills.max_capacity - user_skills.current_workload) / user_skills.max_capacity
            
            # Combined score
            total_score = skill_score * 0.7 + workload_score * 0.3
            
            candidates.append((member.id, total_score))
        
        # Return the best candidate
        if candidates:
            candidates.sort(key=lambda x: x[1], reverse=True)
            best_user_id = candidates[0][0]
            
            # Update workload
            self.user_skills[best_user_id].current_workload += 1
            
            return best_user_id
            
        return None  # No suitable assignee found
    
    def _get_required_skills(self, labels: List[str]) -> List[str]:
        """Convert issue labels to required skills"""
        label_to_skill = {
            "frontend": ["frontend", "ui"],
            "backend": ["backend", "api"],
            "mobile": ["mobile", "android", "ios"],
            "bug": ["testing", "debugging"],
            "enhancement": ["development"],
            "urgent": ["senior"]  # Urgent issues go to experienced people
        }
        
        required = []
        for label in labels:
            if label in label_to_skill:
                required.extend(label_to_skill[label])
        
        return required if required else ["general"]
    
    def _calculate_skill_match(self, user_skills: List[str], required_skills: List[str]) -> float:
        """Calculate how well a user's skills match the requirements"""
        if not required_skills:
            return 0.5  # Neutral score
            
        matches = len(set(user_skills) & set(required_skills))
        return matches / len(required_skills)

# Example usage with smart assignment
def demo_smart_assignment():
    """Demo showing automatic assignment and labeling"""
    print("🧠 Smart Assignment Demo")
    print("=" * 40)
    
    # Create users
    alice = User(id=1, username="alice", name="Alice Smith", email="alice@example.com")
    bob = User(id=2, username="bob", name="Bob Johnson", email="bob@example.com")
    charlie = User(id=3, username="charlie", name="Charlie Brown", email="charlie@example.com")
    
    # Create project
    project = Project(
        id=1,
        name="smart-app",
        description="An app with smart assignment",
        members=[alice, bob, charlie]
    )
    
    # Set up smart assigner
    assigner = SmartAssigner()
    
    # Define team skills (this is realistic - different people have different strengths)
    assigner.add_user_skills(alice.id, ["frontend", "ui", "mobile", "senior"], max_capacity=3)
    assigner.add_user_skills(bob.id, ["backend", "api", "debugging"], max_capacity=4) 
    assigner.add_user_skills(charlie.id, ["testing", "mobile", "general"], max_capacity=5)
    
    # Create issues WITHOUT manual assignment
    raw_issues = [
        {
            "title": "App crashes when opening camera",
            "description": "Critical bug: Users report the mobile app crashes immediately when they try to access the camera feature on Android devices"
        },
        {
            "title": "Add dark mode support to user interface", 
            "description": "Feature request: Implement dark theme for better user experience during nighttime usage"
        },
        {
            "title": "API endpoint returns wrong data format",
            "description": "Backend issue: The /users endpoint is returning XML instead of JSON, breaking the mobile app integration"
        }
    ]
    
    # Process each issue with smart assignment
    for i, issue_data in enumerate(raw_issues, 1):
        print(f"\n📝 Processing Issue #{i}: {issue_data['title']}")
        
        # Auto-generate labels
        labels = assigner.auto_assign_labels(issue_data['title'], issue_data['description'])
        print(f"   🏷️  Auto-assigned labels: {labels}")
        
        # Create issue
        issue = Issue(
            id=i,
            title=issue_data['title'],
            description=issue_data['description'],
            project_id=project.id,
            author_id=alice.id,  # Alice is the product manager creating issues
            labels=labels
        )
        
        # Auto-assign to best person
        assignee_id = assigner.find_best_assignee(issue, project)
        if assignee_id:
            issue.assignee_id = assignee_id
            assignee_name = next(user.name for user in project.members if user.id == assignee_id)
            print(f"   👤 Auto-assigned to: {assignee_name}")
            
            # Show why this person was chosen
            user_skills = assigner.user_skills[assignee_id]
            print(f"   💡 Reason: Skills {user_skills.skills}, Workload: {user_skills.current_workload}/{user_skills.max_capacity}")
        else:
            print(f"   ❌ No suitable assignee found (team at capacity)")
        
        project.issues.append(issue)
    
    print(f"\n📊 FINAL TEAM WORKLOAD:")
    for member in project.members:
        if member.id in assigner.user_skills:
            skills = assigner.user_skills[member.id]
            print(f"   {member.name}: {skills.current_workload}/{skills.max_capacity} issues")

if __name__ == "__main__":
    demo_smart_assignment()