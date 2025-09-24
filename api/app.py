# === api/app.py ===
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from api.routes.user import router as user_router
from api.routes.project import router as project_router
from api.routes.issues import router as issues_router
from database.connection import init_database

app = FastAPI(
    title="GitLab MCP Simulator",
    description="A GitLab-like simulator for AI model training and testing",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_database()

# Include routers
app.include_router(user_router, prefix="/api/v1", tags=["users"])
app.include_router(project_router, prefix="/api/v1", tags=["projects"])
app.include_router(issues_router, prefix="/api/v1", tags=["issues"])

@app.get("/")
async def root():
    return {
        "message": "GitLab MCP Simulator API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}