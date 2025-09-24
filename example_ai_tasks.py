# === example_ai_tasks.py ===
"""
Example AI training tasks for the GitLab MCP Simulator.
These demonstrate the types of project management scenarios AI models can practice.
"""

import requests
import json
from typing import List, Dict

BASE_URL = "http://localhost:8000/api/v1"

class GitLabAITasks:
    """Example AI tasks for project management training"""
    
    def task_1_triage_new_issues(self):
        """Task: Auto-assign labels and assignees to new issues"""
        print("🎯 AI Task 1: Issue Triage")
        
        # Get all unassigned issues
        response = requests.get(f"{BASE_URL}/issues?assignee_id=null")
        issues = response.json()
        
        print(f"Found {len(issues)} unassigned issues to triage")
        
        # Get available users
        users_response = requests.get(f"{BASE_URL}/users")
        users = users_response.json()
        
        for issue in issues[:3]:  # Process first 3 issues
            print(f"\nTriaging issue #{issue['id']}: {issue['title']}")
            
            # AI would analyze title/description and decide:
            suggested_labels = self._suggest_labels(issue['title'], issue['description'])
            suggested_assignee = self._suggest_assignee(issue, users)
            
            # Update the issue
            update_data = {
                "labels": suggested_labels,
                "assignee_id": suggested_assignee
            }
            
            update_response = requests.patch(
                f"{BASE_URL}/issues/{issue['id']}", 
                json=update_data
            )
            
            if update_response.status_code == 200:
                assignee_name = next((u['name'] for u in users if u['id'] == suggested_assignee), "None")
                print(f"  ✅ Labels: {suggested_labels}")
                print(f"  ✅ Assigned to: {assignee_name}")
            else:
                print(f"  ❌ Failed to update issue")
    
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
            from_user = overloaded[0]
            to_user = underloaded[0]
            
            print(f"\nReassigning issues from {from_user['name']} to {to_user['name']}")
            
            # This would be the AI's decision-making process
            response = requests.post(
                f"{BASE_URL}/admin/bulk-reassign",
                params={
                    "from_user_id": from_user['username'].split('_')[0],  # Simplified lookup
                    "to_user_id": to_user['username'].split('_')[0]
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✅ {result['message']}")
    
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
            status = "🟢 Healthy" if health_score > 70 else "🟡 At Risk" if health_score > 40 else "🔴 Critical"
            
            print(f"\n{project['name']}: {status} ({health_score}%)")
            print(f"  Total Issues: {project['issues_count']}")
            print(f"  Open Issues: {project['open_issues_count']}")
            
            if project['open_issues_count'] > 5:
                print(f"  ⚠️  High number of open issues")
            
            # AI would provide recommendations
            recommendations = self._generate_recommendations(project)
            if recommendations:
                print(f"  💡 Recommendations:")
                for rec in recommendations:
                    print(f"     • {rec}")
    
    def _suggest_labels(self, title: str, description: str) -> List[str]:
        """Simulate AI label suggestion"""
        content = (title + " " + description).lower()
        labels = []
        
        if any(word in content for word in ["bug", "error", "crash", "broken"]):
            labels.append("bug")
        if any(word in content for word in ["feature", "add", "new", "implement"]):
            labels.append("enhancement")
        if any(word in content for word in ["urgent", "critical", "asap"]):
            labels.append("urgent")
        if any(word in content for word in ["mobile", "android", "ios"]):
            labels.append("mobile")
        if any(word in content for word in ["ui", "interface", "design"]):
            labels.append("frontend")
        
        return labels if labels else ["general"]
    
    def _suggest_assignee(self, issue: Dict, users: List[Dict]) -> int:
        """Simulate AI assignee suggestion"""
        # Simple logic: assign to user with least work
        # Real AI would consider skills, availability, etc.
        return users[0]['id'] if users else None
    
    def _calculate_health_score(self, project: Dict) -> int:
        """Calculate project health score (0-100)"""
        total_issues = project['issues_count']
        open_issues = project['open_issues_count']
        
        if total_issues == 0:
            return 100
        
        # Simple scoring: fewer open issues = healthier
        completion_rate = ((total_issues - open_issues) / total_issues) * 100
        
        # Penalize projects with too many total issues
        if total_issues > 10:
            completion_rate *= 0.8
        
        return int(completion_rate)
    
    def _generate_recommendations(self, project: Dict) -> List[str]:
        """Generate AI recommendations"""
        recommendations = []
        
        if project['open_issues_count'] > 5:
            recommendations.append("Consider closing stale issues")
            recommendations.append("Review workload distribution")
        
        if project['issues_count'] == 0:
            recommendations.append("Add initial project tasks")
        
        return recommendations

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
        
        print("\n🎉 AI Training Demo Completed!")
        print("💡 These tasks help AI models learn real project management skills")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API server.")
        print("💡 Make sure the server is running: python main.py")

if __name__ == "__main__":
    run_ai_training_demo()