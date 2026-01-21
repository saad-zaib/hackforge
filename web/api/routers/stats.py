from fastapi import APIRouter, HTTPException, Depends
from dependencies import get_database, generator, orchestrator
from config import CORE_PATH
import logging

router = APIRouter(prefix="/api", tags=["stats"])
logger = logging.getLogger(__name__)

def require_db():
    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    return db

@router.get("/stats")
async def get_statistics(db=Depends(require_db)):
    """Get platform statistics"""
    platform_stats = db.get_platform_stats()

    # Get blueprints count
    try:
        blueprints = generator.list_blueprints()
        platform_stats['total_blueprints'] = len(blueprints)
    except Exception as e:
        logger.error(f"Failed to count blueprints: {e}")
        platform_stats['total_blueprints'] = 0

    # Get machines count
    try:
        machines = orchestrator.list_machines()
        platform_stats['total_machines'] = len(machines)
    except Exception as e:
        logger.error(f"Failed to count machines: {e}")
        platform_stats['total_machines'] = 0

    return platform_stats

@router.get("/leaderboard")
async def get_leaderboard(limit: int = 100, timeframe: str = 'all_time', db=Depends(require_db)):
    """Get leaderboard"""
    leaderboard = db.get_leaderboard(limit=limit, timeframe=timeframe)
    return {
        'timeframe': timeframe,
        'entries': leaderboard
    }
