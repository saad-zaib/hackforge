"""
Hackforge Web API with Database Integration
Enhanced API with user tracking and progress
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sys
import os
from pathlib import Path
import json
import time
import uuid

# Add parent directories to path
sys.path.append(str(Path(__file__).parent.parent.parent / "core"))
sys.path.append(str(Path(__file__).parent.parent.parent / "docker" / "orchestrator"))
sys.path.append(str(Path(__file__).parent.parent / "database"))

from generator import HackforgeGenerator
from template_engine import TemplateEngine
from orchestrator import DockerOrchestrator
from base import MachineConfig

# Import database
try:
    sys.path.append(str(Path(__file__).parent.parent / "database"))
    from database import get_db
except ImportError:
    print("Warning: Database module not found. Install dependencies:")
    print("  pip3 install pymongo motor")
    print("  Or run without database using main.py")
    sys.exit(1)

# Initialize components
app = FastAPI(
    title="Hackforge API",
    description="REST API for Dynamic Vulnerability Training Platform with Database",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

generator = HackforgeGenerator()
template_engine = TemplateEngine()
orchestrator = DockerOrchestrator()
db = get_db()


# ============================================================================
# Pydantic Models
# ============================================================================

class UserCreate(BaseModel):
    username: str
    email: str
    role: str = "student"

class FlagSubmitRequest(BaseModel):
    machine_id: str
    flag: str
    user_id: str

class CampaignCreateRequest(BaseModel):
    user_id: str
    difficulty: int = 2
    count: Optional[int] = None


# ============================================================================
# User Endpoints
# ============================================================================

@app.post("/api/users")
async def create_user(user: UserCreate):
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
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/users/{user_id}")
async def get_user(user_id: str):
    """Get user details"""
    user = db.get_user(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get user's rank
    rank = db.get_user_rank(user_id)
    user['rank'] = rank
    
    return user

@app.get("/api/users/{user_id}/progress")
async def get_user_progress(user_id: str):
    """Get user's overall progress"""
    
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    campaigns = db.get_user_campaigns(user_id)
    
    # Get recent submissions
    submissions = db.get_user_submissions(user_id, limit=10)
    
    return {
        'user': user,
        'campaigns': campaigns,
        'recent_submissions': submissions
    }


# ============================================================================
# Campaign Endpoints with Database
# ============================================================================

@app.post("/api/campaigns")
async def create_campaign(request: CampaignCreateRequest, background_tasks: BackgroundTasks):
    """Create a new campaign with database tracking"""
    
    # Validate difficulty
    if not 1 <= request.difficulty <= 5:
        raise HTTPException(status_code=400, detail="Difficulty must be between 1 and 5")
    
    # Check if user exists, create if not
    user = db.get_user(request.user_id)
    if not user:
        user_data = {
            'user_id': request.user_id,
            'username': request.user_id,
            'email': f"{request.user_id}@hackforge.local",
            'role': 'student'
        }
        db.create_user(user_data)
    
    # Generate campaign
    machines = generator.generate_campaign(
        user_id=request.user_id,
        difficulty=request.difficulty,
        count=request.count
    )
    
    if not machines:
        raise HTTPException(status_code=500, detail="Failed to generate campaign")
    
    # Export campaign
    campaign_path = generator.export_campaign(machines)
    campaign_id = Path(campaign_path).name
    
    # Generate applications
    machine_infos = template_engine.generate_campaign_apps(campaign_path)
    
    # Store in database
    campaign_data = {
        'campaign_id': campaign_id,
        'user_id': request.user_id,
        'difficulty': request.difficulty,
        'machine_count': len(machines),
        'machines': [
            {
                'machine_id': m.machine_id,
                'variant': m.variant,
                'difficulty': m.difficulty,
                'blueprint_id': m.blueprint_id,
                'flag': m.flag['content'],
                'port': machine_infos[i]['port'] if i < len(machine_infos) else None
            }
            for i, m in enumerate(machines)
        ]
    }
    
    db.create_campaign(campaign_data)
    
    # Create progress records for each machine
    for machine in machines:
        progress_data = {
            'user_id': request.user_id,
            'machine_id': machine.machine_id,
            'campaign_id': campaign_id
        }
        db.create_progress(progress_data)
    
    return {
        'campaign_id': campaign_id,
        'user_id': request.user_id,
        'difficulty': request.difficulty,
        'machines': campaign_data['machines'],
        'status': 'created'
    }

@app.get("/api/campaigns/{campaign_id}/progress")
async def get_campaign_progress(campaign_id: str, user_id: str):
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


# ============================================================================
# Flag Validation with Database
# ============================================================================


@app.post("/api/flags/validate")
async def validate_flag(request: FlagSubmitRequest, req: Request):
    """Validate flag with database tracking"""

    # Try to find machine in orchestrator (running containers)
    machines = orchestrator.list_machines()
    target_machine = None

    for machine in machines:
        if machine['machine_id'] == request.machine_id:
            target_machine = machine
            break

    # If not found in orchestrator, check database campaigns
    if not target_machine:
        # Search through all campaigns for this machine
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
        # Create progress if doesn't exist
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
        # Calculate points
        points = target_machine['difficulty'] * 100

        # Check if first solve
        if not progress.get('solved', False):
            # Mark as solved
            solve_time = int((time.time() - progress['started_at'].timestamp()))
            db.mark_solved(request.user_id, request.machine_id, points, solve_time)

            # Update user stats
            db.add_points(request.user_id, points)
            db.increment_solved(request.user_id)

            # Update campaign progress
            campaign_id = progress.get('campaign_id')
            if campaign_id and campaign_id != 'unknown':
                campaign_progress = db.get_campaign_progress(request.user_id, campaign_id)
                solved_count = sum(1 for p in campaign_progress if p.get('solved', False))
                total_points = sum(p.get('points_earned', 0) for p in campaign_progress)

                db.update_campaign_progress(campaign_id, solved_count, total_points)

                # Check if campaign completed
                campaign = db.get_campaign(campaign_id)
                if solved_count == campaign['machine_count']:
                    db.complete_campaign(campaign_id)

            submission_data['points_awarded'] = points

            message = f"🎉 Correct! First solve! +{points} points"
        else:
            message = "✅ Flag already captured"
    else:
        message = "❌ Incorrect flag. Try again!"

    # Record submission
    db.record_submission(submission_data)

    return {
        'correct': correct,
        'message': message,
        'points': submission_data['points_awarded']
    }


# ============================================================================
# BLUEPRINTS ENDPOINTS - FIXED
# ============================================================================

@app.get("/api/blueprints")
async def list_blueprints():
    """List all available blueprints"""
    try:
        blueprints = generator.list_blueprints()

        return [
            {
                "blueprint_id": bp.blueprint_id,
                "name": bp.name,
                "category": bp.category,
                "description": bp.description,
                "difficulty_range": bp.difficulty_range,
                "variants": [
                    v.variant_id if hasattr(v, 'variant_id') else v
                    for v in (bp.variants if hasattr(bp, 'variants') else [])
                ],
                "technologies": bp.technologies if hasattr(bp, 'technologies') else []
            }
            for bp in blueprints
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/blueprints/{blueprint_id}")
async def get_blueprint(blueprint_id: str):
    """Get specific blueprint details"""
    try:
        blueprints = generator.list_blueprints()
        blueprint = next((bp for bp in blueprints if bp.blueprint_id == blueprint_id), None)
        
        if not blueprint:
            raise HTTPException(status_code=404, detail="Blueprint not found")
        
        return {
            "blueprint_id": blueprint.blueprint_id,
            "name": blueprint.name,
            "category": blueprint.category,
            "description": blueprint.description,
            "difficulty_range": blueprint.difficulty_range,
            "variants": [
                {
                    "variant_id": v.variant_id,
                    "name": v.name,
                    "description": v.description,
                    "technology": v.technology
                }
                for v in blueprint.variants
            ],
            "entry_points": blueprint.entry_points,
            "mutation_axes": blueprint.mutation_axes,
            "technologies": blueprint.technologies
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Leaderboard Endpoints
# ============================================================================

@app.get("/api/leaderboard")
async def get_leaderboard(
    limit: int = 100,
    timeframe: str = 'all_time'
):
    """Get leaderboard"""
    
    leaderboard = db.get_leaderboard(limit=limit, timeframe=timeframe)
    
    return {
        'timeframe': timeframe,
        'entries': leaderboard
    }


# ============================================================================
# Statistics with Database
# ============================================================================


@app.get("/api/stats")
async def get_statistics():
    """Get platform statistics from database"""

    platform_stats = db.get_platform_stats()
    
    # Add total_blueprints count
    try:
        blueprints = generator.list_blueprints()
        platform_stats['total_blueprints'] = len(blueprints)
    except Exception:
        platform_stats['total_blueprints'] = 0
    
    # Add total_machines count
    try:
        machines = orchestrator.list_machines()
        platform_stats['total_machines'] = len(machines)
    except Exception:
        platform_stats['total_machines'] = 0

    return platform_stats


# ============================================================================
# Machine Endpoints (ADD THESE)
# ============================================================================

@app.get("/api/machines")
async def list_machines():
    """List all generated machines"""
    machines = orchestrator.list_machines()
    
    return [
        {
            'machine_id': m['machine_id'],
            'variant': m['variant'],
            'difficulty': m['difficulty'],
            'blueprint_id': m['blueprint_id'],
            'flag': m['flag']
        }
        for m in machines
    ]

@app.get("/api/machines/{machine_id}")
async def get_machine(machine_id: str):
    """Get specific machine details"""
    machines = orchestrator.list_machines()
    
    for machine in machines:
        if machine['machine_id'] == machine_id:
            # Load full config
            config_file = Path(machine['directory']) / "config.json"
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            return config
    
    raise HTTPException(status_code=404, detail="Machine not found")

# Add this temporarily to your main_with_db.py to get better error details

@app.get("/api/machines/{machine_id}/stats")
async def get_machine_statistics(machine_id: str):
    """Get statistics for a specific machine"""
    try:
        stats = db.get_machine_stats(machine_id)
        return stats
    except Exception as e:
        import traceback
        print(f"ERROR in get_machine_statistics: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error getting machine stats: {str(e)}")

@app.get("/api/statistics")
async def get_statistics_alias():
    """Get platform statistics (alias for /api/stats)"""
    platform_stats = db.get_platform_stats()
    
    # Add total_blueprints count
    try:
        blueprints = generator.list_blueprints()
        platform_stats['total_blueprints'] = len(blueprints)
    except Exception:
        platform_stats['total_blueprints'] = 0
    
    return platform_stats

@app.post("/api/validate-flag/{machine_id}")
async def validate_flag_by_path(machine_id: str, request: Request):
    """Validate flag with machine_id in path (alternative endpoint)"""
    
    # Get request body
    body = await request.json()
    flag = body.get('flag', '')
    user_id = body.get('user_id', 'unknown')
    
    # Create FlagSubmitRequest object
    flag_request = FlagSubmitRequest(
        machine_id=machine_id,
        flag=flag,
        user_id=user_id
    )
    
    # Call existing validation function
    return await validate_flag(flag_request, request)
# ============================================================================
# Docker Management Endpoints (ADD THESE)
# ============================================================================

@app.post("/api/docker/start")
async def start_containers(background_tasks: BackgroundTasks):
    """Start all Docker containers"""
    
    def start_async():
        orchestrator.start_machines(build=True, detached=True)
    
    background_tasks.add_task(start_async)
    
    return {
        "message": "Starting containers in background",
        "status": "building"
    }

@app.post("/api/docker/stop")
async def stop_containers():
    """Stop all Docker containers"""
    success = orchestrator.stop_machines()
    
    if success:
        return {"message": "Containers stopped successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to stop containers")

@app.post("/api/docker/restart")
async def restart_containers():
    """Restart all Docker containers"""
    success = orchestrator.restart_machines()
    
    if success:
        return {"message": "Containers restarted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to restart containers")

@app.get("/api/docker/status")
async def docker_status():
    """Get Docker container status"""
    containers = orchestrator.status_machines()
    
    return {
        "containers": containers,
        "total": len(containers),
        "running": sum(1 for c in containers if c.get('State') == 'running')
    }

@app.delete("/api/docker/destroy")
async def destroy_containers():
    """Destroy all Docker containers"""
    success = orchestrator.destroy_machines(remove_volumes=True)
    
    if success:
        return {"message": "Containers destroyed successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to destroy containers")
# ============================================================================
# Health Check
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check with database status"""
    
    try:
        # Test database connection
        db.users.find_one()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "database": db_status,
        "timestamp": time.time()
    }


if __name__ == "__main__":
    import uvicorn
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║          HACKFORGE WEB API WITH DATABASE                  ║
╚═══════════════════════════════════════════════════════════╝

Starting API server with MongoDB integration...
    """)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
