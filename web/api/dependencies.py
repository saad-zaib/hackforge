import sys
import logging
from pathlib import Path
from .config import CORE_PATH, DOCKER_PATH, DATABASE_PATH, GENERATED_MACHINES_DIR

logger = logging.getLogger(__name__)

# Add paths to sys.path
sys.path.insert(0, str(CORE_PATH))
sys.path.insert(0, str(DOCKER_PATH))
sys.path.insert(0, str(DATABASE_PATH))

# Import core components
from generator import DynamicHackforgeGenerator
from template_engine import TemplateEngine
from orchestrator import DockerOrchestrator

# Initialize core components (these don't require DB)
generator = DynamicHackforgeGenerator(core_dir=str(CORE_PATH))
template_engine = TemplateEngine()
orchestrator = DockerOrchestrator(machines_dir=str(GENERATED_MACHINES_DIR))

logger.info("✓ Core components initialized")

# Database - LAZY INITIALIZATION (only when needed)
_db_instance = None

def get_database():
    """
    Lazy database initialization.
    Returns None if MongoDB is not available.
    This allows the API to start even if MongoDB is down.
    """
    global _db_instance
    
    if _db_instance is None:
        try:
            from database import get_db
            _db_instance = get_db()
            logger.info("✓ Database connected")
        except Exception as e:
            logger.warning(f"⚠ Database not available: {e}")
            logger.warning("⚠ API will run in limited mode without database")
            _db_instance = None
    
    return _db_instance
