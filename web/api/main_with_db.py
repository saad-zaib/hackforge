"""
Hackforge Web API with Database Integration
FIXED VERSION - Correct paths for your project structure
"""

import docker
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
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FIXED: Correct path structure for your project
# Your structure: forge/web/api/main_with_db.py
# Core is at: forge/core/

PROJECT_ROOT = Path(__file__).parent.parent.parent  # Goes up to forge/
CORE_PATH = PROJECT_ROOT / "core"
DOCKER_PATH = PROJECT_ROOT / "docker" / "orchestrator"
DATABASE_PATH = Path(__file__).parent.parent / "database"

logger.info(f"Project root: {PROJECT_ROOT}")
logger.info(f"Core path: {CORE_PATH}")
logger.info(f"Docker path: {DOCKER_PATH}")

# Add correct paths to sys.path
sys.path.insert(0, str(CORE_PATH))
sys.path.insert(0, str(DOCKER_PATH))
sys.path.insert(0, str(DATABASE_PATH))

from generator import HackforgeGenerator
from template_engine import TemplateEngine
from orchestrator import DockerOrchestrator
from base import MachineConfig

# Import database
try:
    from database import get_db
except ImportError as e:
    logger.error(f"Failed to import database: {e}")
    print("Warning: Database module not found. Install dependencies:")
    print("  pip3 install pymongo motor")
    sys.exit(1)

# Initialize components with correct paths
app = FastAPI(
    title="Hackforge API",
    description="REST API for Dynamic Vulnerability Training Platform with Database",
    version="2.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize with correct paths
generator = HackforgeGenerator(blueprints_dir=str(CORE_PATH / "blueprints"))
template_engine = TemplateEngine()

# FIXED: Point orchestrator to correct machines directory
# Campaigns are stored in: forge/core/campaigns/campaign_XXX/
orchestrator = DockerOrchestrator(machines_dir=str(CORE_PATH / "campaigns"))

db = get_db()

logger.info("✓ All components initialized")


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
    campaign_name: str
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
    submissions = db.get_user_submissions(user_id, limit=10)

    return {
        'user': user,
        'campaigns': campaigns,
        'recent_submissions': submissions
    }

@app.get("/api/users/{user_id}/campaigns")
async def get_user_campaigns_list(user_id: str):
    """Get list of user's campaigns"""
    try:
        logger.info(f"Fetching campaigns for user: {user_id}")
        campaigns = db.get_user_campaigns(user_id)
        logger.info(f"Found {len(campaigns)} campaigns")
        
        # Add progress info to each campaign
        for campaign in campaigns:
            try:
                # Remove MongoDB _id field if present (not JSON serializable)
                if '_id' in campaign:
                    del campaign['_id']
                
                progress_list = db.get_campaign_progress(user_id, campaign['campaign_id'])
                solved = sum(1 for p in progress_list if p.get('solved', False))
                campaign['machines_solved'] = solved
                campaign['progress_percentage'] = (solved / campaign['machine_count'] * 100) if campaign['machine_count'] > 0 else 0
            except Exception as e:
                logger.error(f"Error processing campaign {campaign.get('campaign_id')}: {e}")
                campaign['machines_solved'] = 0
                campaign['progress_percentage'] = 0
        
        logger.info(f"Successfully processed {len(campaigns)} campaigns")
        return campaigns
    except Exception as e:
        logger.error(f"Error in get_user_campaigns_list: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to fetch campaigns: {str(e)}")


# ============================================================================
# Campaign Endpoints with Database
# ============================================================================

@app.post("/api/campaigns")
async def create_campaign(request: CampaignCreateRequest, background_tasks: BackgroundTasks):
    """Create a new campaign with database tracking"""
    
    logger.info("=" * 60)
    logger.info(f"CREATING CAMPAIGN: {request.campaign_name}")
    logger.info(f"User: {request.user_id}, Difficulty: {request.difficulty}, Count: {request.count}")

    # Validate difficulty
    if not 1 <= request.difficulty <= 5:
        raise HTTPException(status_code=400, detail="Difficulty must be between 1 and 5")
    
    # Validate campaign name
    if not request.campaign_name or len(request.campaign_name.strip()) == 0:
        raise HTTPException(status_code=400, detail="Campaign name is required")

    # Check if user exists, create if not
    user = db.get_user(request.user_id)
    if not user:
        logger.info("Creating default user...")
        user_data = {
            'user_id': request.user_id,
            'username': request.user_id,
            'email': f"{request.user_id}@hackforge.local",
            'role': 'student'
        }
        db.create_user(user_data)

    # Generate campaign
    logger.info("Generating machines...")
    try:
        machines = generator.generate_campaign(
            user_id=request.user_id,
            difficulty=request.difficulty,
            count=request.count
        )
        logger.info(f"✓ Generated {len(machines)} machines")
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate campaign: {str(e)}")

    if not machines:
        raise HTTPException(status_code=500, detail="Failed to generate campaign")

    # Export campaign - this creates the campaign folder in forge/core/campaigns/
    logger.info("Exporting campaign...")
    campaign_path = generator.export_campaign(machines)
    campaign_id = Path(campaign_path).name
    logger.info(f"✓ Campaign exported to: {campaign_path}")

    # Generate applications
    logger.info("Generating Docker applications...")
    try:
        machine_infos = template_engine.generate_campaign_apps(campaign_path)
        logger.info(f"✓ Generated {len(machine_infos)} apps")
    except Exception as e:
        logger.warning(f"Failed to generate apps: {e}")
        machine_infos = []

    # Prepare campaign data for database
    campaign_data = {
        'campaign_id': campaign_id,
        'campaign_name': request.campaign_name,
        'user_id': request.user_id,
        'difficulty': request.difficulty,
        'machine_count': len(machines),
        'status': 'active',
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

    # Save to database
    logger.info("Saving to MongoDB...")
    try:
        db.create_campaign(campaign_data)
        logger.info("✓ Saved to database")
    except Exception as e:
        logger.error(f"Database save failed: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    # Create progress records
    logger.info("Creating progress records...")
    for machine in machines:
        try:
            progress_data = {
                'user_id': request.user_id,
                'machine_id': machine.machine_id,
                'campaign_id': campaign_id
            }
            db.create_progress(progress_data)
        except Exception as e:
            logger.warning(f"Progress record failed for {machine.machine_id}: {e}")

    logger.info("✓ Campaign creation complete!")
    logger.info("=" * 60)

    return {
        'campaign_id': campaign_id,
        'campaign_name': request.campaign_name,
        'user_id': request.user_id,
        'difficulty': request.difficulty,
        'machines': campaign_data['machines'],
        'status': 'created'
    }

@app.get("/api/campaigns/{campaign_id}")
async def get_campaign_details(campaign_id: str):
    """Get detailed information about a specific campaign"""
    campaign = db.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Get progress for this campaign
    progress_list = db.get_campaign_progress(campaign['user_id'], campaign_id)
    
    # Add progress info to each machine
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

@app.get("/api/campaigns/{campaign_id}/machines")
async def get_campaign_machines(campaign_id: str):
    """Get all machines for a specific campaign"""
    campaign = db.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    return {
        'campaign_id': campaign_id,
        'campaign_name': campaign.get('campaign_name', 'Unnamed Campaign'),
        'machines': campaign.get('machines', [])
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


# ============================================================================
# BLUEPRINTS ENDPOINTS
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
                "variants": bp.variants,
                "technologies": getattr(bp, 'technologies', [])
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
            "variants": blueprint.variants,
            "entry_points": blueprint.entry_points,
            "mutation_axes": blueprint.mutation_axes,
            "technologies": getattr(blueprint, 'technologies', [])
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Leaderboard Endpoints
# ============================================================================

@app.get("/api/leaderboard")
async def get_leaderboard(limit: int = 100, timeframe: str = 'all_time'):
    """Get leaderboard"""
    leaderboard = db.get_leaderboard(limit=limit, timeframe=timeframe)
    return {
        'timeframe': timeframe,
        'entries': leaderboard
    }


# ============================================================================
# Statistics
# ============================================================================

@app.get("/api/stats")
async def get_statistics():
    """Get platform statistics from database"""
    platform_stats = db.get_platform_stats()

    try:
        blueprints = generator.list_blueprints()
        platform_stats['total_blueprints'] = len(blueprints)
    except Exception:
        platform_stats['total_blueprints'] = 0

    try:
        machines = orchestrator.list_machines()
        platform_stats['total_machines'] = len(machines)
    except Exception:
        platform_stats['total_machines'] = 0

    return platform_stats


# ============================================================================
# Machine Endpoints
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
            config_file = Path(machine['directory']) / "config.json"
            with open(config_file, 'r') as f:
                config = json.load(f)
            return config

    raise HTTPException(status_code=404, detail="Machine not found")

@app.get("/api/machines/{machine_id}/stats")
async def get_machine_statistics(machine_id: str):
    """Get statistics for a specific machine"""
    try:
        stats = db.get_machine_stats(machine_id)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting machine stats: {str(e)}")


# ============================================================================
# Docker Management - BULK OPERATIONS
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
# Individual Container Management
# ============================================================================

@app.post("/api/docker/container/{container_id}/start")
async def start_container(container_id: str):
    """Start a specific container"""
    try:
        import docker
        client = docker.from_env()
        container = client.containers.get(container_id)

        if container.status == 'running':
            return {"message": "Container is already running", "status": "running"}

        container.start()
        return {"message": f"Container {container.name} started successfully", "status": "started"}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail=f"Container {container_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start container: {str(e)}")

@app.post("/api/docker/container/{container_id}/stop")
async def stop_container(container_id: str):
    """Stop a specific container"""
    try:
        import docker
        client = docker.from_env()
        container = client.containers.get(container_id)

        if container.status != 'running':
            return {"message": "Container is already stopped", "status": "stopped"}

        container.stop(timeout=10)
        return {"message": f"Container {container.name} stopped successfully", "status": "stopped"}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail=f"Container {container_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop container: {str(e)}")

@app.post("/api/docker/container/{container_id}/restart")
async def restart_container(container_id: str):
    """Restart a specific container"""
    try:
        import docker
        client = docker.from_env()
        container = client.containers.get(container_id)
        container.restart(timeout=10)
        return {"message": f"Container {container.name} restarted successfully", "status": "restarted"}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail=f"Container {container_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to restart container: {str(e)}")

@app.delete("/api/docker/container/{container_id}")
async def remove_container(container_id: str):
    """Remove a specific container"""
    try:
        import docker
        client = docker.from_env()
        container = client.containers.get(container_id)
        container.remove(force=True)
        return {"message": f"Container removed successfully", "status": "removed"}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail=f"Container {container_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove container: {str(e)}")

@app.get("/api/docker/container/{container_id}/logs")
async def get_container_logs(container_id: str, tail: int = 100):
    """Get logs from a specific container"""
    try:
        import docker
        client = docker.from_env()
        container = client.containers.get(container_id)
        logs = container.logs(tail=tail, timestamps=True).decode('utf-8')
        return {"logs": logs, "container_id": container_id}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail=f"Container {container_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get logs: {str(e)}")

@app.get("/api/docker/campaign/{campaign_id}/containers")
async def get_campaign_containers(campaign_id: str):
    """Get all Docker containers for a specific campaign"""
    try:
        import docker
        client = docker.from_env()
        
        campaign = db.get_campaign(campaign_id)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        all_containers = client.containers.list(all=True)
        campaign_machine_ids = [m['machine_id'] for m in campaign.get('machines', [])]
        
        campaign_containers = []
        for container in all_containers:
            container_name = container.name
            for machine_id in campaign_machine_ids:
                if machine_id[:12] in container_name or machine_id in container_name:
                    campaign_containers.append({
                        'Id': container.id,
                        'Name': container.name,
                        'State': container.status,
                        'Status': container.status,
                        'Image': container.image.tags[0] if container.image.tags else 'unknown',
                        'machine_id': machine_id
                    })
                    break
        
        return {
            'campaign_id': campaign_id,
            'campaign_name': campaign.get('campaign_name', 'Unknown'),
            'containers': campaign_containers,
            'total': len(campaign_containers),
            'running': sum(1 for c in campaign_containers if c['State'] == 'running')
        }
    except docker.errors.DockerException as e:
        raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ============================================================================
# Health Check
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check with database status"""
    try:
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
