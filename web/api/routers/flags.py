from fastapi import APIRouter, HTTPException, Request, Depends
from dependencies import get_database, orchestrator
from schemas.flag import FlagSubmitRequest
import uuid
import time
import logging

router = APIRouter(prefix="/api/flags", tags=["flags"])
logger = logging.getLogger(__name__)

def require_db():
    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    return db

@router.post("/validate")
async def validate_flag(request: FlagSubmitRequest, req: Request, db=Depends(require_db)):
    """Validate flag with database tracking"""
    
    # Find machine
    machines = orchestrator.list_machines()
    target_machine = None

    for machine in machines:
        if machine['machine_id'] == request.machine_id:
            target_machine = machine
            break

    # Check database if not found
    if not target_machine:
        all_campaigns = db.campaigns.find()

        for campaign in all_campaigns:
            for machine in campaign.get('machines', []):
                if machine['machine_id'] == request.machine_id:
                    target_machine = {
                        'machine_id': machine['machine_id'],
                        'variant': machine['variant'],
                        'difficulty': machine['difficulty'],
                        'blueprint_id': machine['blueprint_id'],
                        'flag': machine['flag']
                    }
                    break
            if target_machine:
                break

    if not target_machine:
        raise HTTPException(
            status_code=404,
            detail=f"Machine not found: {request.machine_id}"
        )

    # Get or create progress
    progress = db.get_progress(request.user_id, request.machine_id)

    if not progress:
        progress_data = {
            'user_id': request.user_id,
            'machine_id': request.machine_id,
            'campaign_id': 'unknown'
        }
        progress = db.create_progress(progress_data)

    # Increment attempt
    db.increment_attempts(request.user_id, request.machine_id)

    # Validate flag
    correct = request.flag.strip() == target_machine['flag'].strip()

    # Record submission
    submission_data = {
        'submission_id': f"sub_{uuid.uuid4().hex[:16]}",
        'user_id': request.user_id,
        'machine_id': request.machine_id,
        'campaign_id': progress.get('campaign_id', 'unknown'),
        'submitted_flag': request.flag,
        'correct': correct,
        'ip_address': req.client.host,
        'points_awarded': 0
    }

    if correct:
        points = target_machine['difficulty'] * 100

        if not progress.get('solved', False):
            solve_time = int((time.time() - progress['started_at'].timestamp()))
            db.mark_solved(request.user_id, request.machine_id, points, solve_time)
            db.add_points(request.user_id, points)
            db.increment_solved(request.user_id)

            campaign_id = progress.get('campaign_id')
            if campaign_id and campaign_id != 'unknown':
                campaign_progress = db.get_campaign_progress(request.user_id, campaign_id)
                solved_count = sum(1 for p in campaign_progress if p.get('solved', False))
                total_points = sum(p.get('points_earned', 0) for p in campaign_progress)

                db.update_campaign_progress(campaign_id, solved_count, total_points)

                campaign = db.get_campaign(campaign_id)
                if solved_count == campaign['machine_count']:
                    db.complete_campaign(campaign_id)

            submission_data['points_awarded'] = points
            message = f"🎉 Correct! First solve! +{points} points"
        else:
            message = "✅ Flag already captured"
    else:
        message = "❌ Incorrect flag. Try again!"

    db.record_submission(submission_data)

    return {
        'correct': correct,
        'message': message,
        'points': submission_data['points_awarded']
    }
