# === main.py ===
"""
GitLab MCP Simulator - Main Entry Point
Run this file to start the simulator and test everything works
"""

from core.models import User, Project, Issue, Label, IssueState, ProjectVisibility
from datetime import datetime

def main():
    """Main function to test our simulator"""
    print("🚀 Starting GitLab MCP Simulator...")
    print("=" * 50)
    
    # Test our models work
    print("1. Creating users...")
    alice = User(id=1, username="alice", name="Alice Smith", email="alice@example.com")
    bob = User(id=2, username="bob", name="Bob Johnson", email="bob@example.com")
    charlie = User(id=3, username="charlie", name="Charlie Brown", email="charlie@example.com")
    
    print(f"   ✅ Created users: {alice.name}, {bob.name}, {charlie.name}")
    
    # Test creating labels
    print("2. Creating labels...")
    bug_label = Label(id=1, name="bug", color="FF0000", description="Something isn't working")
    feature_label = Label(id=2, name="enhancement", color="00FF00", description="New feature request")
    urgent_label = Label(id=3, name="urgent", color="FF8800", description="Needs immediate attention")
    
    print(f"   ✅ Created {len([bug_label, feature_label, urgent_label])} labels")
    
    # Test creating a project
    print("3. Creating project...")
    project = Project(
        id=1,
        name="awesome-mobile-app",
        description="A mobile app that will change the world!",
        visibility=ProjectVisibility.PRIVATE,
        owner_id=alice.id,
        members=[alice, bob, charlie],
        labels=[bug_label, feature_label, urgent_label]
    )
    print(f"   ✅ Created project: '{project.name}' with {len(project.members)} members")
    
    # Test creating issues
    print("4. Creating issues...")
    issues = [
        Issue(
            id=1,
            title="App crashes on startup",
            description="When users open the app, it immediately crashes on Android 12+",
            project_id=project.id,
            author_id=alice.id,
            assignee_id=bob.id,
            labels=["bug", "urgent"]
        ),
        Issue(
            id=2,
            title="Add dark mode support",
            description="Users have requested dark mode for better nighttime usage",
            project_id=project.id,
            author_id=charlie.id,
            assignee_id=alice.id,
            labels=["enhancement"]
        ),
        Issue(
            id=3,
            title="Improve app loading speed",
            description="App takes 5+ seconds to load, should be under 2 seconds",
            project_id=project.id,
            author_id=bob.id,
            labels=["enhancement"]
        )
    ]
    
    # Add issues to project
    project.issues.extend(issues)
    print(f"   ✅ Created {len(issues)} issues")
    
    # Display summary
    print("\n📊 PROJECT SUMMARY:")
    print("=" * 50)
    print(f"Project: {project.name}")
    print(f"Description: {project.description}")
    print(f"Members: {len(project.members)}")
    print(f"Total Issues: {len(project.issues)}")
    
    print(f"\n📋 ISSUES:")
    for issue in project.issues:
        assignee_name = next((user.name for user in project.members if user.id == issue.assignee_id), "Unassigned")
        print(f"  • [{issue.id}] {issue.title}")
        print(f"    Assigned to: {assignee_name}")
        print(f"    Labels: {', '.join(issue.labels)}")
        print(f"    Status: {issue.state.value}")
        print()
    
    print("🎉 Simulator test completed successfully!")
    print("All core components are working properly.")

if __name__ == "__main__":
    main()