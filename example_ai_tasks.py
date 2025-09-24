"""
Example AI training tasks for the GitLab MCP Simulator.
These demonstrate the types of project management scenarios AI models can practice.
"""
import requests
from typing import List, Dict

BASE_URL = "http://localhost:8000/api/v1"

class GitLabAITasks:
    """Example AI tasks for project management training"""
    
    def task_1_triage_new_issues(self):
        """Task: Auto-assign labels and assignees to new issues"""
        print("🎯 AI Task 1: Issue Triage")
        
        # Get all issues and filter for unassigned
        response = requests.get(f"{BASE_URL}/issues")
        issues = response.json()
        unassigned_issues = [issue for issue in issues if issue.get('assignee_id') is None]
        
        print(f"Found {len(unassigned_issues)} unassigned issues to triage")
        
        # Defensive: ensure issues is a list
        if not isinstance(unassigned_issues, list):
            print("❌ Unexpected response from /issues endpoint:", unassigned_issues)
            return
        
        # Get available users
        users_response = requests.get(f"{BASE_URL}/users")
        users = users_response.json()
        
        for issue in unassigned_issues[:3]:  # Process first 3 issues
            print(f"\nTriaging issue #{issue['id']}: {issue['title']}")
            suggested_labels = self._suggest_labels(issue['title'], issue['description'])
            suggested_assignee = self._suggest_assignee(issue, users)
            print(f"Suggested labels: {suggested_labels}")
            print(f"Suggested assignee: {suggested_assignee}")
            # Simulate updating the issue
            update_data = {
                "labels": suggested_labels,
                "assignee_id": suggested_assignee
            }
            patch_resp = requests.patch(f"{BASE_URL}/issues/{issue['id']}", json=update_data)
            if patch_resp.status_code == 200:
                print("✅ Issue updated!")
            else:
                print("❌ Failed to update issue:", patch_resp.text)
    
    def task_2_workload_balancing(self):
        """Task: Balance workload across team members"""
        print("\n🎯 AI Task 2: Workload Balancing")
        
        # Get system stats to see current workload
        stats_response = requests.get(f"{BASE_URL}/admin/stats")
        stats = stats_response.json()
        
        print("Current workload distribution:")
        workload = stats['workload_distribution']
        
        # Find overloaded and underloaded users
        overloaded = [w for w in workload if w['assigned_issues'] > 3]
        underloaded = [w for w in workload if w['assigned_issues'] < 2]
        
        print(f"Overloaded users: {len(overloaded)}")
        print(f"Underloaded users: {len(underloaded)}")
        
        # Demonstrate bulk reassignment (AI would choose optimal transfers)
        if overloaded and underloaded:
            from_user_id = overloaded[0]['id']
            to_user_id = underloaded[0]['id']
            print(f"Reassigning issues from {overloaded[0]['name']} to {underloaded[0]['name']}")
            reassign_resp = requests.post(
                f"{BASE_URL}/admin/bulk-reassign",
                params={"from_user_id": from_user_id, "to_user_id": to_user_id, "limit": 2}
            )
            print("Bulk reassignment result:", reassign_resp.json())
        else:
            print("No suitable users for reassignment demo.")
    
    def task_3_project_health_report(self):
        """Task: Generate project health insights"""
        print("\n🎯 AI Task 3: Project Health Analysis")
        
        # Get all projects with stats
        projects_response = requests.get(f"{BASE_URL}/projects")
        projects = projects_response.json()
        
        print("Project Health Report:")
        print("-" * 40)
        
        for project in projects:
            health_score = self._calculate_health_score(project)
            recommendations = self._generate_recommendations(project)
            print(f"Project: {project['name']}")
            print(f"  Health Score: {health_score}/100")
            print(f"  Recommendations: {', '.join(recommendations)}")
            print("-" * 40)
    
    def _suggest_labels(self, title: str, description: str) -> List[str]:
        """Simulate AI label suggestion"""
        content = (title + " " + description).lower()
        labels = []
        
        if any(word in content for word in ["bug", "error", "crash", "broken"]):
            labels.append("bug")
        if any(word in content for word in ["feature", "add", "new", "implement"]):
            labels.append("feature")
        if any(word in content for word in ["urgent", "critical", "asap"]):
            labels.append("urgent")
        if any(word in content for word in ["mobile", "android", "ios"]):
            labels.append("mobile")
        if any(word in content for word in ["ui", "interface", "design"]):
            labels.append("ui")
        
        return labels if labels else ["general"]
    
    def _suggest_assignee(self, issue: Dict, users: List[Dict]) -> int:
        """Simulate AI assignee suggestion"""
        # Assign to first available user for demo
        if users:
            return users[0]['id']
        return None
    
    def _calculate_health_score(self, project: Dict) -> int:
        """Simulate project health scoring"""
        total_issues = project.get('total_issues', 0)
        open_issues = project.get('open_issues', 0)
        if total_issues == 0:
            return 100
        closed = total_issues - open_issues
        score = int((closed / total_issues) * 100)
        return score
    
    def _generate_recommendations(self, project: Dict) -> List[str]:
        """Simulate AI recommendations for project health"""
        recs = []
        if project.get('open_issues', 0) > 5:
            recs.append("Reduce open issues")
        if project.get('total_issues', 0) == 0:
            recs.append("Add more issues to start work")
        if not recs:
            recs.append("Project is healthy")
        return recs

def run_ai_training_demo():
    """Run a demo of AI training tasks"""
    print("🤖 GitLab MCP Simulator - AI Training Demo")
    print("=" * 50)
    print("This demonstrates the types of tasks AI models can practice")
    print()
    
    try:
        tasks = GitLabAITasks()
        tasks.task_1_triage_new_issues()
        tasks.task_2_workload_balancing()
        tasks.task_3_project_health_report()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API server.")
        print("💡 Make sure the server is running: python main.py")

if __name__ == "__main__":
    run_ai_training_demo()