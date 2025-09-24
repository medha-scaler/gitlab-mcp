# === config.py ===
import os
from pathlib import Path

DATABASE_URL = "sqlite:///gitlab_simulator.db"
PROJECT_ROOT = Path(__file__).parent