from pathlib import Path
import logging

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
CORE_PATH = PROJECT_ROOT / "core"
DOCKER_PATH = PROJECT_ROOT / "docker" / "orchestrator"
DATABASE_PATH = Path(__file__).parent.parent / "database"
GENERATED_MACHINES_DIR = CORE_PATH / "generated_machines"

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# CORS settings
CORS_ORIGINS = ["*"]

# API settings
API_TITLE = "Hackforge API"
API_VERSION = "2.1.0"
