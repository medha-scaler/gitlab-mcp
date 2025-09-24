# === test_api.py (Testing script) ===
"""
Test script to verify the GitLab MCP Simulator is working correctly.
Run this after starting the server to test all endpoints.
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api/v1"

def test_api():
    """Test all major API endpoints"""
    print("🧪 Testing GitLab MCP Simulator API")
    print("=" * 40)
    
    # Test 1: Get all users
    print("1. Testing GET /users")
    response = requests.get(f"{BASE_URL}/users")
    if response.status_code == 200:
        users = response.json()
        print(f"   ✅ Found {len(users)} users")
        user_id = users[0]['id'] if users else None
    else:
        print(f"   ❌ Failed: {response.status_code}")
        return
    
    # Test 2: Get all projects
    print("2. Testing GET /projects")
    response = requests.get(f"{BASE_URL}/projects")
    if response.status_code == 200:
        projects = response.json()
        print(f"   ✅ Found {len(projects)} projects")
        project_id = projects[0]['id'] if projects else None
    else:
        print(f"   ❌ Failed: {response.status_code}")
        return
    
    # Test 3: Get all issues
    print("3. Testing GET /issues")
    response = requests.get(f"{BASE_URL}/issues")
    if response.status_code == 200:
        issues = response.json()
        print(f"   ✅ Found {len(issues)} issues")
    else:
        print(f"   ❌ Failed: {response.status_code}")
        return
    
    # Test 4: Create a new issue
    print("4. Testing POST /issues (create)")
    if project_id and user_id:
        new_issue = {
            "title": "Test API Issue",
            "description": "This is a test issue created by the test script",
            "project_id": project_id,
            "labels": ["test", "api"]
        }
        response = requests.post(
            f"{BASE_URL}/issues?author_id={user_id}",
            json=new_issue
        )
        if response.status_code == 200:
            created_issue = response.json()
            print(f"   ✅ Created issue #{created_issue['id']}: {created_issue['title']}")
            test_issue_id = created_issue['id']
        else:
            print(f"   ❌ Failed to create issue: {response.status_code}")
            print(f"   Error: {response.text}")
            test_issue_id = None
    
    # Test 5: Update an issue
    if test_issue_id:
        print("5. Testing PATCH /issues (update)")
        update_data = {
            "state": "closed",
            "labels": ["test", "api", "completed"]
        }
        response = requests.patch(
            f"{BASE_URL}/issues/{test_issue_id}",
            json=update_data
        )
        if response.status_code == 200:
            updated_issue = response.json()
            print(f"   ✅ Updated issue state to: {updated_issue['state']}")
        else:
            print(f"   ❌ Failed to update issue: {response.status_code}")
    
    # Test 6: Get system stats
    print("6. Testing GET /admin/stats")
    response = requests.get(f"{BASE_URL}/admin/stats")
    if response.status_code == 200:
        stats = response.json()
        print(f"   ✅ System stats:")
        print(f"      Users: {stats['users']}")
        print(f"      Projects: {stats['projects']}")
        print(f"      Total Issues: {stats['issues']['total']}")
        print(f"      Open Issues: {stats['issues']['open']}")
    else:
        print(f"   ❌ Failed to get stats: {response.status_code}")
    
    print("\n🎉 API testing completed!")
    print("💡 Try the interactive docs at: http://localhost:8000/docs")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API server.")
        print("💡 Make sure the server is running: python main.py")