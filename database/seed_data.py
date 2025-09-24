# === database/seed_data.py ===
import json
import random
from database.connection import DatabaseManager

def seed_sample_data():
    """Seed database with realistic sample data for AI training"""
    
    # Check if data already exists
    existing_users = DatabaseManager.execute_query("SELECT COUNT(*) as count FROM users")
    if existing_users[0]['count'] > 0:
        print("📊 Database already contains data, skipping seed")
        return
    
    print("🌱 Seeding sample data...")
    
    # Seed Users (Enterprise team with global distribution)
    users_data = [
        ("john_doe", "John Doe", "john.doe@company.com", "https://avatar.example.com/john.png"),
        ("sarah_chen", "Sarah Chen", "sarah.chen@company.com", "https://avatar.example.com/sarah.png"),
        ("mike_wilson", "Mike Wilson", "mike.wilson@company.com", "https://avatar.example.com/mike.png"),
        ("priya_sharma", "Priya Sharma", "priya.sharma@company.com", "https://avatar.example.com/priya.png"),
        ("alex_rodriguez", "Alex Rodriguez", "alex.rodriguez@company.com", "https://avatar.example.com/alex.png"),
        ("emma_taylor", "Emma Taylor", "emma.taylor@company.com", "https://avatar.example.com/emma.png"),
        ("david_kim", "David Kim", "david.kim@company.com", "https://avatar.example.com/david.png"),
        ("lisa_brown", "Lisa Brown", "lisa.brown@company.com", "https://avatar.example.com/lisa.png"),
    ]
    
    user_ids = []
    for username, name, email, avatar in users_data:
        user_id = DatabaseManager.execute_insert(
            "INSERT INTO users (username, name, email, avatar_url) VALUES (?, ?, ?, ?)",
            (username, name, email, avatar)
        )
        user_ids.append(user_id)
    
    print(f"✅ Created {len(user_ids)} users")
    
    # Seed Projects (Realistic enterprise projects)
    projects_data = [
        ("E-Commerce Platform", "Main customer-facing web application", "public", user_ids[0]),
        ("Mobile App Backend", "REST API for iOS and Android apps", "private", user_ids[1]),
        ("Analytics Dashboard", "Internal business intelligence dashboard", "internal", user_ids[2]),
        ("Payment Gateway", "Secure payment processing system", "private", user_ids[3]),
        ("Customer Support Portal", "Help desk and ticket management", "internal", user_ids[4]),
        ("Inventory Management", "Warehouse and stock tracking system", "private", user_ids[5]),
    ]
    
    project_ids = []
    for name, desc, visibility, owner_id in projects_data:
        project_id = DatabaseManager.execute_insert(
            "INSERT INTO projects (name, description, visibility, owner_id) VALUES (?, ?, ?, ?)",
            (name, desc, visibility, owner_id)
        )
        project_ids.append(project_id)
    
    print(f"✅ Created {len(project_ids)} projects")
    
    # Seed Issues (Realistic enterprise issues with varying complexity)
    issues_data = [
        # E-Commerce Platform issues
        ("Login page not responsive on mobile", "Users report login form breaks on screens < 768px", project_ids[0], user_ids[0], user_ids[1], "opened", ["bug", "mobile", "frontend"]),
        ("Implement two-factor authentication", "Add 2FA support for enhanced security", project_ids[0], user_ids[1], user_ids[2], "opened", ["enhancement", "security"]),
        ("Shopping cart persists after logout", "Cart items remain visible after user logs out", project_ids[0], user_ids[2], user_ids[1], "opened", ["bug", "security"]),
        ("Add product recommendation engine", "ML-based product suggestions on product pages", project_ids[0], user_ids[3], None, "opened", ["enhancement", "ml", "feature"]),
        ("Fix checkout payment timeout", "Payment processing times out after 30 seconds", project_ids[0], user_ids[4], user_ids[3], "closed", ["bug", "payment", "urgent"]),
        
        # Mobile App Backend issues
        ("API rate limiting not working", "Rate limits not enforced on authentication endpoints", project_ids[1], user_ids[1], user_ids[4], "opened", ["bug", "api", "security"]),
        ("Add push notification service", "Implement FCM/APNS for mobile notifications", project_ids[1], user_ids[2], user_ids[5], "opened", ["enhancement", "mobile"]),
        ("Database connection pooling", "Optimize DB connections under high load", project_ids[1], user_ids[5], user_ids[1], "opened", ["performance", "database"]),
        
        # Analytics Dashboard issues
        ("Dashboard loading takes >10 seconds", "Performance issues with large datasets", project_ids[2], user_ids[2], user_ids[6], "opened", ["bug", "performance"]),
        ("Add real-time data refresh", "Auto-refresh dashboard every 30 seconds", project_ids[2], user_ids[6], None, "opened", ["enhancement", "real-time"]),
        ("Export to CSV broken", "CSV export generates malformed files", project_ids[2], user_ids[7], user_ids[2], "closed", ["bug", "export"]),
        
        # Payment Gateway issues
        ("PCI compliance audit", "Ensure system meets PCI DSS standards", project_ids[3], user_ids[3], user_ids[7], "opened", ["compliance", "security", "urgent"]),
        ("Add cryptocurrency support", "Support Bitcoin and Ethereum payments", project_ids[3], user_ids[4], None, "opened", ["enhancement", "crypto"]),
        
        # Customer Support Portal issues  
        ("Ticket search not working", "Search returns no results for valid queries", project_ids[4], user_ids[4], user_ids[0], "opened", ["bug", "search"]),
        ("Add automated ticket routing", "Route tickets based on category and urgency", project_ids[4], user_ids[0], user_ids[4], "opened", ["enhancement", "automation"]),
        
        # Inventory Management issues
        ("Low stock alerts not sent", "Email notifications failing for inventory < 10", project_ids[5], user_ids[5], user_ids[3], "opened", ["bug", "alerts"]),
        ("Barcode scanner integration", "Add support for handheld barcode scanners", project_ids[5], user_ids[6], user_ids[5], "opened", ["enhancement", "hardware"]),
    ]
    
    issue_ids = []
    for title, desc, project_id, author_id, assignee_id, state, labels in issues_data:
        labels_json = json.dumps(labels)
        issue_id = DatabaseManager.execute_insert(
            "INSERT INTO issues (title, description, project_id, author_id, assignee_id, state, labels) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (title, desc, project_id, author_id, assignee_id, state, labels_json)
        )
        issue_ids.append(issue_id)
    
    print(f"✅ Created {len(issue_ids)} issues")
    print("🎉 Sample data seeding completed!")
    print("💡 This simulates a real enterprise environment with 2+ years of usage")