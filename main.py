# === Updated main.py ===
import uvicorn
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from database.seed_data import seed_sample_data
from database.connection import init_database

def main():
    """Initialize and start the GitLab MCP Simulator"""
    print("🔧 Initializing GitLab MCP Simulator...")
    print("=" * 50)
    
    try:
        # Setup database
        print("📁 Setting up database...")
        init_database()
        seed_sample_data()
        print("✅ Database setup complete!")
        
        print("\n🌐 Starting API server...")
        print("📖 Swagger docs: http://localhost:8000/docs")
        print("📋 ReDoc docs: http://localhost:8000/redoc")
        print("💻 API base URL: http://localhost:8000/api/v1")
        print("\n🎯 Ready for AI model training!")
        print("=" * 50)
        
        # Start the server
        uvicorn.run(
            "api.app:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except Exception as e:
        print(f"❌ Failed to start simulator: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()