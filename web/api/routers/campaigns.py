from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from dependencies import get_database
from schemas.campaign import CampaignCreateRequest
from services.campaign_service import CampaignService
from services.docker_service import DockerService
from pathlib import Path
import logging

router = APIRouter(prefix="/api/campaigns", tags=["campaigns"])
logger = logging.getLogger(__name__)

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
async def create_campaign(
    request: CampaignCreateRequest, 
    background_tasks: BackgroundTasks,
    db=Depends(require_db)
):
    """Create a new campaign"""
    try:
        campaign_data, campaign_path = CampaignService.create_campaign(
            user_id=request.user_id,
            campaign_name=request.campaign_name,
            difficulty=request.difficulty,
            count=request.count
        )
        
        # Start containers
        containers_started = DockerService.start_campaign_containers(Path(campaign_path))
        
        return {
            **campaign_data,
            'status': 'created',
            'containers_started': containers_started
        }
        
    except Exception as e:
        logger.error(f"Campaign creation failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{campaign_id}")
async def get_campaign(campaign_id: str, db=Depends(require_db)):
    """Get campaign details"""
    campaign = db.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    progress_list = db.get_campaign_progress(campaign['user_id'], campaign_id)
    
    # Add progress to machines
    for machine in campaign.get('machines', []):
        machine_progress = next(
            (p for p in progress_list if p['machine_id'] == machine['machine_id']),
            None
        )
        if machine_progress:
            machine['solved'] = machine_progress.get('solved', False)
            machine['attempts'] = machine_progress.get('attempts', 0)
            machine['points_earned'] = machine_progress.get('points_earned', 0)
        else:
            machine['solved'] = False
            machine['attempts'] = 0
            machine['points_earned'] = 0
    
    # Calculate overall progress
    total_machines = campaign['machine_count']
    solved = sum(1 for p in progress_list if p.get('solved', False))
    total_points = sum(p.get('points_earned', 0) for p in progress_list)
    
    campaign['progress'] = {
        'solved': solved,
        'total': total_machines,
        'percentage': (solved / total_machines * 100) if total_machines > 0 else 0,
        'total_points': total_points
    }
    
    return campaign

@router.get("/{campaign_id}/machines")
async def get_campaign_machines(campaign_id: str, db=Depends(require_db)):
    """Get all machines for a specific campaign"""
    campaign = db.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    return {
        'campaign_id': campaign_id,
        'campaign_name': campaign.get('campaign_name', 'Unnamed Campaign'),
        'machines': campaign.get('machines', [])
    }

@router.get("/{campaign_id}/progress")
async def get_campaign_progress(campaign_id: str, user_id: str, db=Depends(require_db)):
    """Get progress for a specific campaign"""
    campaign = db.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    progress_list = db.get_campaign_progress(user_id, campaign_id)

    total_machines = campaign['machine_count']
    solved = sum(1 for p in progress_list if p.get('solved', False))
    progress_percentage = (solved / total_machines * 100) if total_machines > 0 else 0

    return {
        'campaign': campaign,
        'progress': progress_list,
        'summary': {
            'total_machines': total_machines,
            'solved': solved,
            'percentage': round(progress_percentage, 2)
        }
    }
