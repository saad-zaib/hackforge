from fastapi import APIRouter, HTTPException, Depends
from dependencies import get_database  # CHANGED: Import function, not db directly
from schemas.user import UserCreate
import uuid
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/users", tags=["users"])

def require_db():
    """Dependency that ensures database is available"""
    db = get_database()
    if db is None:
        raise HTTPException(
            status_code=503, 
            detail="Database not available. Please start MongoDB."
        )
    return db

@router.post("")
async def create_user(user: UserCreate, db=Depends(require_db)):  # CHANGED: Use dependency
    """Create a new user"""
    user_id = f"user_{uuid.uuid4().hex[:12]}"
    
    user_data = {
        'user_id': user_id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'total_points': 0,
        'machines_solved': 0,
        'campaigns_completed': 0
    }
    
    try:
        created_user = db.create_user(user_data)
        return created_user
    except Exception as e:
        logger.error(f"Failed to create user: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}")
async def get_user(user_id: str, db=Depends(require_db)):  # CHANGED: Use dependency
    """Get user details"""
    user = db.get_user(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    rank = db.get_user_rank(user_id)
    user['rank'] = rank
    
    return user

@router.get("/{user_id}/campaigns")
async def get_user_campaigns(user_id: str, db=Depends(require_db)):  # CHANGED: Use dependency
    """Get user's campaigns"""
    try:
        campaigns = db.get_user_campaigns(user_id)
        
        for campaign in campaigns:
            if '_id' in campaign:
                del campaign['_id']
            
            progress_list = db.get_campaign_progress(user_id, campaign['campaign_id'])
            solved = sum(1 for p in progress_list if p.get('solved', False))
            campaign['machines_solved'] = solved
            campaign['progress_percentage'] = (
                (solved / campaign['machine_count'] * 100) 
                if campaign['machine_count'] > 0 else 0
            )
        
        return campaigns
    except Exception as e:
        logger.error(f"Failed to get campaigns: {e}")
        raise HTTPException(status_code=500, detail=str(e))
