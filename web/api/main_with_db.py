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
import yaml
import subprocess
from pathlib import Path

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

from generator import DynamicHackforgeGenerator
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
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=[
        "http://4.231.90.52:3000",
        "http://localhost:3000",
        "http://0.0.0.0:3000",
    ],
)

# Initialize with correct paths
generator = DynamicHackforgeGenerator(core_dir=str(CORE_PATH))
template_engine = TemplateEngine()

# FIXED: Point orchestrator to correct machines directory
# Campaigns are stored in: forge/core/campaigns/campaign_XXX/
GENERATED_MACHINES_DIR = CORE_PATH / "generated_machines"
orchestrator = DockerOrchestrator(machines_dir=str(GENERATED_MACHINES_DIR))

logger.info(f"Orchestrator watching: {GENERATED_MACHINES_DIR}")

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
    selected_blueprints: Optional[List[str]] = None


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

def start_campaign_containers(campaign_path: Path):
    """
    Start Docker containers for a campaign
    """
    try:
        import subprocess

        compose_file = campaign_path / "docker-compose.yml"

        if not compose_file.exists():
            logger.warning(f"No docker-compose.yml found in {campaign_path}")
            return False

        logger.info(f"Starting containers for {campaign_path.name}...")

        # Run docker-compose up -d --build
        result = subprocess.run(
            ["docker-compose", "up", "-d", "--build"],
            cwd=str(campaign_path),
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        if result.returncode == 0:
            logger.info(f"✓ Containers started successfully")
            return True
        else:
            logger.error(f"✗ Failed to start containers: {result.stderr}")
            return False

    except Exception as e:
        logger.error(f"Error starting containers: {e}")
        return False

@app.post("/api/campaigns")
async def create_campaign(request: CampaignCreateRequest, background_tasks: BackgroundTasks):
    """Create a new campaign with database tracking"""

    logger.info("=" * 60)
    logger.info(f"CREATING CAMPAIGN: {request.campaign_name}")
    logger.info(f"User: {request.user_id}, Difficulty: {request.difficulty}, Count: {request.count}")
    logger.info(f"Selected Blueprints: {request.selected_blueprints}")

    # Generate campaign
    logger.info("Generating machines...")
    try:
        # NEW: Pass selected blueprints to generator
        machines = generator.generate_campaign(
            user_id=request.user_id,
            difficulty=request.difficulty,
            count=request.count,
            blueprint_ids=request.selected_blueprints  # Pass selected blueprints
        )
        logger.info(f"✓ Generated {len(machines)} machines")
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to generate campaign: {str(e)}")

    if not machines:
        raise HTTPException(status_code=500, detail="No machines were generated")

    # FIXED: Create campaign-specific directory
    campaign_id = f"campaign_{int(time.time())}"
    campaign_output_dir = f"campaigns/{campaign_id}"

    logger.info(f"Campaign ID: {campaign_id}")
    logger.info("Exporting campaign...")

    try:
        # Export with specific campaign directory
        campaign_path = generator.export_campaign(machines, output_dir=campaign_output_dir)
        logger.info(f"✓ Campaign exported to: {campaign_path}")
    except Exception as e:
        logger.error(f"Export failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to export campaign: {str(e)}")

    # Generate applications
    logger.info("Generating Docker applications...")
    try:
        machine_infos = template_engine.generate_campaign_apps(campaign_path)
        logger.info(f"✓ Generated {len(machine_infos)} apps")
    except Exception as e:
        logger.warning(f"Failed to generate apps: {e}")
        import traceback
        logger.error(traceback.format_exc())
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

    # ✨ NEW: Start Docker containers automatically
    logger.info("Starting Docker containers...")
    try:
        containers_started = start_campaign_containers(Path(campaign_path))
        if containers_started:
            logger.info("✓ Docker containers started successfully")
        else:
            logger.warning("⚠ Failed to start containers automatically")
    except Exception as e:
        logger.warning(f"⚠ Could not start containers: {e}")
        # Don't fail the entire campaign creation if containers fail to start

    logger.info("✓ Campaign creation complete!")
    logger.info("=" * 60)

    return {
        'campaign_id': campaign_id,
        'campaign_name': request.campaign_name,
        'user_id': request.user_id,
        'difficulty': request.difficulty,
        'machines': campaign_data['machines'],
        'status': 'created',
        'containers_started': containers_started if 'containers_started' in locals() else False
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


@app.delete("/api/campaigns/{campaign_id}")
async def delete_campaign(campaign_id: str):
    """Delete a campaign and all its associated data"""
    try:
        import docker
        import shutil

        logger.info(f"Deleting campaign: {campaign_id}")

        # Get campaign from database
        campaign = db.get_campaign(campaign_id)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")

        # Step 1: Stop and remove all Docker containers
        try:
            client = docker.from_env()
            containers = client.containers.list(all=True)

            for machine in campaign.get('machines', []):
                machine_id = machine['machine_id']

                # Find and remove container
                for container in containers:
                    if machine_id[:12] in container.name or machine_id in container.name:
                        try:
                            logger.info(f"Removing container: {container.name}")
                            container.remove(force=True)
                        except Exception as e:
                            logger.warning(f"Failed to remove container {container.name}: {e}")
                        break
        except Exception as e:
            logger.error(f"Error removing containers: {e}")

        # Step 2: Delete campaign directory from filesystem
        try:
            campaign_path = CORE_PATH / "campaigns" / campaign_id
            if campaign_path.exists():
                logger.info(f"Removing campaign directory: {campaign_path}")
                shutil.rmtree(campaign_path)
        except Exception as e:
            logger.error(f"Error removing campaign directory: {e}")

        # Step 3: Delete from database
        try:
            # Delete progress records
            db.progress.delete_many({'campaign_id': campaign_id})

            # Delete submissions
            db.submissions.delete_many({'campaign_id': campaign_id})

            # Delete campaign
            db.campaigns.delete_one({'campaign_id': campaign_id})

            logger.info(f"✓ Campaign {campaign_id} deleted from database")
        except Exception as e:
            logger.error(f"Error deleting from database: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

        return {
            'message': 'Campaign deleted successfully',
            'campaign_id': campaign_id,
            'deleted': True
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting campaign: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to delete campaign: {str(e)}")
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


def load_blueprints_directly(blueprints_dir: Path):
    """Load blueprints directly from YAML files"""
    blueprints = []

    if not blueprints_dir.exists():
        logger.warning(f"Blueprints directory not found: {blueprints_dir}")
        return blueprints

    yaml_files = list(blueprints_dir.glob("*_blueprint.yaml"))
    logger.info(f"Loading {len(yaml_files)} blueprint files from {blueprints_dir}")

    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r') as f:
                data = yaml.safe_load(f)

            # Create a simple blueprint object
            class BlueprintObj:
                def __init__(self, data):
                    self.blueprint_id = data.get('blueprint_id', 'unknown')
                    self.name = data.get('name', 'Unknown')
                    self.category = data.get('category', 'unknown')
                    self.description = data.get('description', '')
                    self.difficulty_range = data.get('difficulty_range', [1, 5])
                    self.variants = data.get('variants', [])
                    self.technologies = data.get('technologies', [])
                    self.entry_points = data.get('entry_points', [])
                    self.mutation_axes = data.get('mutation_axes', {})

            blueprint = BlueprintObj(data)
            blueprints.append(blueprint)
            logger.info(f"✓ Loaded blueprint: {blueprint.name} ({blueprint.blueprint_id})")

        except Exception as e:
            logger.error(f"✗ Failed to load {yaml_file.name}: {e}")

    return blueprints


# ============================================================================
# BLUEPRINTS ENDPOINTS
# ============================================================================


@app.get("/api/blueprints")
async def list_blueprints():
    """List all available blueprints"""
    try:
        # Try generator first
        try:
            blueprints = generator.list_blueprints()
            logger.info(f"Generator returned {len(blueprints)} blueprints")
        except Exception as gen_error:
            logger.warning(f"Generator failed: {gen_error}, using direct loading")
            blueprints_dir = CORE_PATH / "blueprints"
            blueprints = load_blueprints_directly(blueprints_dir)

        if not blueprints:
            logger.error("No blueprints found!")
            return []

        result = [
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

        logger.info(f"Returning {len(result)} blueprints to frontend")
        return result

    except Exception as e:
        logger.error(f"Error in list_blueprints: {e}")
        import traceback
        logger.error(traceback.format_exc())
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


"""
UPDATED: Individual Machine Docker Control
Add these endpoints to your main_with_db.py
"""

# Add these imports at the top
import subprocess
from pathlib import Path

# ============================================================================
# INDIVIDUAL MACHINE DOCKER CONTROL - NEW ENDPOINTS
# ============================================================================

@app.post("/api/machines/{machine_id}/docker/start")
async def start_machine_container(machine_id: str):
    """Start specific machine's docker-compose"""
    try:
        # Find machine directory
        machine_dir = CORE_PATH / "generated_machines" / machine_id

        if not machine_dir.exists():
            # Try campaigns directory
            campaigns_dir = CORE_PATH / "campaigns"
            found = False
            for campaign_dir in campaigns_dir.glob("campaign_*"):
                test_dir = campaign_dir / machine_id
                if test_dir.exists():
                    machine_dir = test_dir
                    found = True
                    break

            if not found:
                raise HTTPException(status_code=404, detail=f"Machine directory not found: {machine_id}")

        compose_file = machine_dir / "docker-compose.yml"
        if not compose_file.exists():
            raise HTTPException(status_code=404, detail="docker-compose.yml not found")

        logger.info(f"Starting container for {machine_id} in {machine_dir}")

        # Run docker-compose up
        result = subprocess.run(
            ["docker-compose", "up", "-d", "--build"],
            cwd=str(machine_dir),
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0:
            logger.info(f"✓ Container started: {machine_id}")

            # Get port from docker-compose.yml
            port = None
            with open(compose_file, 'r') as f:
                for line in f:
                    if 'ports:' in line:
                        continue
                    if '"' in line and ':80"' in line:
                        port = line.split('"')[1].split(':')[0]
                        break

            return {
                "success": True,
                "message": f"Container started successfully",
                "machine_id": machine_id,
                "url": f"http://4.231.90.52:{port}" if port else None,
                "logs": result.stdout
            }
        else:
            logger.error(f"Failed to start {machine_id}: {result.stderr}")
            return {
                "success": False,
                "message": "Failed to start container",
                "error": result.stderr
            }

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Container start timeout")
    except Exception as e:
        logger.error(f"Error starting {machine_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/machines/{machine_id}/docker/stop")
async def stop_machine_container(machine_id: str):
    """Stop specific machine's docker-compose"""
    try:
        machine_dir = CORE_PATH / "generated_machines" / machine_id

        if not machine_dir.exists():
            campaigns_dir = CORE_PATH / "campaigns"
            found = False
            for campaign_dir in campaigns_dir.glob("campaign_*"):
                test_dir = campaign_dir / machine_id
                if test_dir.exists():
                    machine_dir = test_dir
                    found = True
                    break

            if not found:
                raise HTTPException(status_code=404, detail=f"Machine directory not found: {machine_id}")

        compose_file = machine_dir / "docker-compose.yml"
        if not compose_file.exists():
            raise HTTPException(status_code=404, detail="docker-compose.yml not found")

        logger.info(f"Stopping container for {machine_id}")

        result = subprocess.run(
            ["docker-compose", "down"],
            cwd=str(machine_dir),
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            logger.info(f"✓ Container stopped: {machine_id}")
            return {
                "success": True,
                "message": "Container stopped successfully",
                "machine_id": machine_id
            }
        else:
            return {
                "success": False,
                "message": "Failed to stop container",
                "error": result.stderr
            }

    except Exception as e:
        logger.error(f"Error stopping {machine_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/machines/{machine_id}/docker/restart")
async def restart_machine_container(machine_id: str):
    """Restart specific machine's docker-compose"""
    try:
        machine_dir = CORE_PATH / "generated_machines" / machine_id

        if not machine_dir.exists():
            campaigns_dir = CORE_PATH / "campaigns"
            found = False
            for campaign_dir in campaigns_dir.glob("campaign_*"):
                test_dir = campaign_dir / machine_id
                if test_dir.exists():
                    machine_dir = test_dir
                    found = True
                    break

            if not found:
                raise HTTPException(status_code=404, detail=f"Machine directory not found: {machine_id}")

        logger.info(f"Restarting container for {machine_id}")

        # Stop
        subprocess.run(
            ["docker-compose", "down"],
            cwd=str(machine_dir),
            capture_output=True,
            timeout=60
        )

        # Start
        result = subprocess.run(
            ["docker-compose", "up", "-d", "--build"],
            cwd=str(machine_dir),
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0:
            return {
                "success": True,
                "message": "Container restarted successfully",
                "machine_id": machine_id
            }
        else:
            return {
                "success": False,
                "message": "Failed to restart container",
                "error": result.stderr
            }

    except Exception as e:
        logger.error(f"Error restarting {machine_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/machines/{machine_id}/docker/status")
async def get_machine_container_status(machine_id: str):
    """Get docker status for specific machine"""
    try:
        machine_dir = CORE_PATH / "generated_machines" / machine_id

        if not machine_dir.exists():
            campaigns_dir = CORE_PATH / "campaigns"
            found = False
            for campaign_dir in campaigns_dir.glob("campaign_*"):
                test_dir = campaign_dir / machine_id
                if test_dir.exists():
                    machine_dir = test_dir
                    found = True
                    break

            if not found:
                raise HTTPException(status_code=404, detail=f"Machine directory not found: {machine_id}")

        result = subprocess.run(
            ["docker-compose", "ps", "--format", "json"],
            cwd=str(machine_dir),
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0 and result.stdout.strip():
            containers = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    try:
                        containers.append(json.loads(line))
                    except:
                        pass

            return {
                "machine_id": machine_id,
                "containers": containers,
                "running": any(c.get('State') == 'running' for c in containers)
            }
        else:
            return {
                "machine_id": machine_id,
                "containers": [],
                "running": False
            }

    except Exception as e:
        logger.error(f"Error getting status for {machine_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/machines/{machine_id}/docker/logs")
async def get_machine_container_logs(machine_id: str, tail: int = 100):
    """Get logs from specific machine's containers"""
    try:
        machine_dir = CORE_PATH / "generated_machines" / machine_id

        if not machine_dir.exists():
            campaigns_dir = CORE_PATH / "campaigns"
            found = False
            for campaign_dir in campaigns_dir.glob("campaign_*"):
                test_dir = campaign_dir / machine_id
                if test_dir.exists():
                    machine_dir = test_dir
                    found = True
                    break

            if not found:
                raise HTTPException(status_code=404, detail=f"Machine directory not found: {machine_id}")

        result = subprocess.run(
            ["docker-compose", "logs", f"--tail={tail}"],
            cwd=str(machine_dir),
            capture_output=True,
            text=True,
            timeout=30
        )

        return {
            "machine_id": machine_id,
            "logs": result.stdout
        }

    except Exception as e:
        logger.error(f"Error getting logs for {machine_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# CAMPAIGN-LEVEL DOCKER CONTROL
# ============================================================================

@app.post("/api/campaigns/{campaign_id}/docker/start")
async def start_campaign_containers(campaign_id: str):
    """Start all containers in a campaign"""
    try:
        campaign = db.get_campaign(campaign_id)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")

        results = []
        campaign_dir = CORE_PATH / "campaigns" / campaign_id

        for machine in campaign.get('machines', []):
            machine_id = machine['machine_id']
            machine_dir = campaign_dir / machine_id

            if machine_dir.exists():
                try:
                    result = subprocess.run(
                        ["docker-compose", "up", "-d", "--build"],
                        cwd=str(machine_dir),
                        capture_output=True,
                        text=True,
                        timeout=300
                    )

                    results.append({
                        "machine_id": machine_id,
                        "success": result.returncode == 0,
                        "message": "Started" if result.returncode == 0 else result.stderr
                    })
                except Exception as e:
                    results.append({
                        "machine_id": machine_id,
                        "success": False,
                        "message": str(e)
                    })

        success_count = sum(1 for r in results if r['success'])

        return {
            "campaign_id": campaign_id,
            "total": len(results),
            "started": success_count,
            "results": results
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/campaigns/{campaign_id}/docker/stop")
async def stop_campaign_containers(campaign_id: str):
    """Stop all containers in a campaign"""
    try:
        campaign = db.get_campaign(campaign_id)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")

        results = []
        campaign_dir = CORE_PATH / "campaigns" / campaign_id

        for machine in campaign.get('machines', []):
            machine_id = machine['machine_id']
            machine_dir = campaign_dir / machine_id

            if machine_dir.exists():
                try:
                    result = subprocess.run(
                        ["docker-compose", "down"],
                        cwd=str(machine_dir),
                        capture_output=True,
                        text=True,
                        timeout=60
                    )

                    results.append({
                        "machine_id": machine_id,
                        "success": result.returncode == 0
                    })
                except Exception as e:
                    results.append({
                        "machine_id": machine_id,
                        "success": False,
                        "message": str(e)
                    })

        success_count = sum(1 for r in results if r['success'])

        return {
            "campaign_id": campaign_id,
            "total": len(results),
            "stopped": success_count,
            "results": results
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# CAMPAIGN-LEVEL DOCKER CONTROL
# ============================================================================

@app.post("/api/campaigns/{campaign_id}/docker/start")
async def start_campaign_containers(campaign_id: str):
    """Start all containers in a campaign"""
    try:
        campaign = db.get_campaign(campaign_id)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")

        results = []
        campaign_dir = CORE_PATH / "campaigns" / campaign_id

        for machine in campaign.get('machines', []):
            machine_id = machine['machine_id']
            machine_dir = campaign_dir / machine_id

            if machine_dir.exists():
                try:
                    result = subprocess.run(
                        ["docker-compose", "up", "-d", "--build"],
                        cwd=str(machine_dir),
                        capture_output=True,
                        text=True,
                        timeout=300
                    )

                    results.append({
                        "machine_id": machine_id,
                        "success": result.returncode == 0,
                        "message": "Started" if result.returncode == 0 else result.stderr
                    })
                except Exception as e:
                    results.append({
                        "machine_id": machine_id,
                        "success": False,
                        "message": str(e)
                    })

        success_count = sum(1 for r in results if r['success'])

        return {
            "campaign_id": campaign_id,
            "total": len(results),
            "started": success_count,
            "results": results
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/campaigns/{campaign_id}/docker/stop")
async def stop_campaign_containers(campaign_id: str):
    """Stop all containers in a campaign"""
    try:
        campaign = db.get_campaign(campaign_id)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")

        results = []
        campaign_dir = CORE_PATH / "campaigns" / campaign_id

        for machine in campaign.get('machines', []):
            machine_id = machine['machine_id']
            machine_dir = campaign_dir / machine_id

            if machine_dir.exists():
                try:
                    result = subprocess.run(
                        ["docker-compose", "down"],
                        cwd=str(machine_dir),
                        capture_output=True,
                        text=True,
                        timeout=60
                    )

                    results.append({
                        "machine_id": machine_id,
                        "success": result.returncode == 0
                    })
                except Exception as e:
                    results.append({
                        "machine_id": machine_id,
                        "success": False,
                        "message": str(e)
                    })

        success_count = sum(1 for r in results if r['success'])

        return {
            "campaign_id": campaign_id,
            "total": len(results),
            "stopped": success_count,
            "results": results
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Statistics
# ============================================================================


@app.get("/api/stats")
async def get_statistics():
    """Get platform statistics from database"""
    platform_stats = db.get_platform_stats()

    # Get blueprints count with fallback
    try:
        try:
            blueprints = generator.list_blueprints()
        except Exception:
            blueprints_dir = CORE_PATH / "blueprints"
            blueprints = load_blueprints_directly(blueprints_dir)

        platform_stats['total_blueprints'] = len(blueprints)
        logger.info(f"✓ Blueprints count: {len(blueprints)}")
    except Exception as e:
        logger.error(f"✗ Failed to count blueprints: {e}")
        platform_stats['total_blueprints'] = 0

    # Get machines count
    try:
        machines = orchestrator.list_machines()
        platform_stats['total_machines'] = len(machines)
        logger.info(f"✓ Machines count: {len(machines)}")
    except Exception as e:
        logger.error(f"✗ Failed to count machines: {e}")
        platform_stats['total_machines'] = 0

    logger.info(f"Stats response: {platform_stats}")
    return platform_stats

# ============================================================================
# Machine Endpoints
# ============================================================================


@app.get("/api/machines")
async def list_machines():
    """
    List all machines with enhanced metadata
    FIXED: Proper docker-py import handling
    """
    try:
        # Get machines from filesystem
        machines = orchestrator.list_machines()
        
        logger.info(f"Found {len(machines)} machines from orchestrator")

        # Import docker properly
        try:
            import docker as docker_module
            client = docker_module.from_env()
            all_containers = client.containers.list(all=True)
            logger.info(f"Found {len(all_containers)} Docker containers")
        except AttributeError as e:
            logger.error(f"Docker import error: {e}")
            # Try alternative import
            try:
                from docker import DockerClient
                client = DockerClient.from_env()
                all_containers = client.containers.list(all=True)
                logger.info(f"Found {len(all_containers)} Docker containers (alternative method)")
            except Exception as e2:
                logger.error(f"Alternative Docker import also failed: {e2}")
                # Fallback: no container info
                all_containers = []
                logger.warning("Continuing without Docker container info")

        # Enrich with database information
        enriched_machines = []

        for machine in machines:
            machine_id = machine['machine_id']
            logger.info(f"\nProcessing machine: {machine_id}")

            # Try to find campaign this machine belongs to
            campaign = db.campaigns.find_one({
                'machines.machine_id': machine_id
            })

            # Get progress if exists
            progress = db.progress.find_one({
                'machine_id': machine_id
            })

            # Find Docker container - IMPROVED MATCHING
            container_info = None
            
            if all_containers:
                # Try multiple matching strategies
                for container in all_containers:
                    container_name = container.name
                    container_id = container.id
                    
                    # Strategy 1: Match by full machine_id in name
                    if machine_id in container_name:
                        logger.info(f"  ✓ Found container by full ID: {container_name}")
                        container_info = {
                            'container_id': container_id,
                            'container_name': container_name,
                            'status': container.status,
                            'ports': container.ports
                        }
                        break
                    
                    # Strategy 2: Match by machine_id prefix (first 12 chars)
                    if machine_id[:12] in container_name:
                        logger.info(f"  ✓ Found container by prefix: {container_name}")
                        container_info = {
                            'container_id': container_id,
                            'container_name': container_name,
                            'status': container.status,
                            'ports': container.ports
                        }
                        break
                    
                    # Strategy 3: Match by hackforge_ prefix with machine_id
                    expected_name = f"hackforge_{machine_id}"
                    if container_name == expected_name:
                        logger.info(f"  ✓ Found container by expected name: {container_name}")
                        container_info = {
                            'container_id': container_id,
                            'container_name': container_name,
                            'status': container.status,
                            'ports': container.ports
                        }
                        break
            
            if not container_info:
                logger.warning(f"  ✗ No container found for machine {machine_id}")
                if all_containers:
                    logger.warning(f"    Available containers: {[c.name for c in all_containers]}")

            enriched_machine = {
                'machine_id': machine['machine_id'],
                'variant': machine['variant'],
                'difficulty': machine['difficulty'],
                'blueprint_id': machine['blueprint_id'],
                'flag': machine['flag'],
                'directory': machine['directory'],
                # Additional database info
                'campaign_id': campaign['campaign_id'] if campaign else None,
                'campaign_name': campaign.get('campaign_name', 'Unknown') if campaign else None,
                # Progress info
                'solved': progress.get('solved', False) if progress else False,
                'attempts': progress.get('attempts', 0) if progress else 0,
                'points_earned': progress.get('points_earned', 0) if progress else 0,
                # Docker info
                'container': container_info,
                'is_running': container_info['status'] == 'running' if container_info else False,
                'url': None  # Will be populated if running
            }

            # Extract URL from container ports - IMPROVED
            if container_info and container_info['status'] == 'running':
                ports = container_info.get('ports', {})
                logger.info(f"  Container ports: {ports}")
                
                # Parse ports more reliably
                for container_port, host_bindings in ports.items():
                    if host_bindings and isinstance(host_bindings, list) and len(host_bindings) > 0:
                        host_port = host_bindings[0].get('HostPort')
                        if host_port:
                            enriched_machine['url'] = f"http://4.231.90.52:{host_port}"
                            logger.info(f"  ✓ URL: {enriched_machine['url']}")
                            break

            enriched_machines.append(enriched_machine)
            logger.info(f"  Machine enriched: container={bool(container_info)}, url={enriched_machine['url']}")

        logger.info(f"\n✓ Returning {len(enriched_machines)} enriched machines")
        return enriched_machines

    except Exception as e:
        logger.error(f"Error listing machines: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to list machines: {str(e)}")


@app.get("/api/machines/{machine_id}") 
async def get_machine(machine_id: str):
    """Get specific machine details with full context"""
    try:
        # Get from orchestrator
        machines = orchestrator.list_machines()
        machine = next((m for m in machines if m['machine_id'] == machine_id), None)

        if not machine:
            raise HTTPException(status_code=404, detail="Machine not found")

        # Load full config
        config_file = Path(machine['directory']) / "config.json"
        with open(config_file, 'r') as f:
            config = json.load(f)

        # Get campaign info
        campaign = db.campaigns.find_one({
            'machines.machine_id': machine_id
        })

        # Get progress
        progress = db.progress.find_one({
            'machine_id': machine_id
        })

        # Get Docker status
        try:
            import docker
            client = docker.from_env()
            containers = client.containers.list(all=True)

            container_info = None
            for container in containers:
                if machine_id[:12] in container.name or machine_id in container.name:
                    container_info = {
                        'container_id': container.id,
                        'container_name': container.name,
                        'status': container.status,
                        'ports': container.ports,
                        'created': container.attrs['Created'],
                        'image': container.image.tags[0] if container.image.tags else 'unknown'
                    }
                    break
        except Exception as e:
            logger.warning(f"Could not get Docker info: {e}")
            container_info = None

        return {
            **config,
            'campaign_id': campaign['campaign_id'] if campaign else None,
            'campaign_name': campaign.get('campaign_name') if campaign else None,
            'progress': progress,
            'container': container_info
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting machine: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/machines/{machine_id}/stats")
async def get_machine_statistics(machine_id: str):
    """Get statistics for a specific machine"""
    try:
        stats = db.get_machine_stats(machine_id)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting machine stats: {str(e)}")



# ============================================================================
# Config & Blueprint Management Endpoints
# ============================================================================

class VulnerabilityConfig(BaseModel):
    vulnerability_id: str
    name: str
    category: str
    difficulty_range: List[int]
    description: str
    infrastructure: Dict[str, Any]
    database_schema: Optional[Dict[str, Any]] = None
    variants: List[Dict[str, Any]]
    entry_points: List[Dict[str, Any]]
    mutation_axes: Dict[str, Any]
    ai_generation_hints: Optional[Dict[str, Any]] = None
    exploit_examples: Optional[List[Dict[str, Any]]] = None

# ============================================================================
# Config & Blueprint Management Endpoints - FIXED PORT ISSUE
# ============================================================================

@app.post("/api/configs/{category}/generate-machine")
async def generate_machine_from_config(category: str, background_tasks: BackgroundTasks):
    """
    FULLY AUTOMATED SINGLE MACHINE: Config → Blueprint → ONE Machine → Docker App
    FIXED: Proper port parameter handling for template engine
    """
    import sys
    import importlib
    import subprocess
    import time

    try:
        logger.info("="*60)
        logger.info(f"SINGLE MACHINE PIPELINE: {category}")
        logger.info("="*60)

        # STEP 1: Generate Blueprint Components (blueprint/mutation/template)
        logger.info("STEP 1: Generating blueprint components...")
        configs_dir = CORE_PATH / "configs"
        config_path = configs_dir / f"{category}.json"

        if not config_path.exists():
            raise HTTPException(status_code=404, detail=f"Config not found: {category}")

        # Load and validate config
        with open(config_path, 'r') as f:
            config_data = json.load(f)

        logger.info(f"Config loaded: {config_data.get('name', 'Unknown')}")
        logger.info(f"Infrastructure: {config_data.get('infrastructure', {})}")
        logger.info(f"Database schema: {'Present' if config_data.get('database_schema') else 'Not required'}")

        # Ensure CORE_PATH is in sys.path
        if str(CORE_PATH) not in sys.path:
            sys.path.insert(0, str(CORE_PATH))

        from vuln_generator import VulnerabilityGenerator

        generator_vuln = VulnerabilityGenerator(str(config_path))
        generator_vuln.generate_all(str(CORE_PATH))

        logger.info("✓ Generated blueprint, mutation, and template")

        # STEP 2: Reload generator to pick up new blueprint
        logger.info("\nSTEP 2: Reloading generator with new blueprint...")

        # Remove cached modules to force reload
        modules_to_reload = ['generator', 'base']
        for mod in modules_to_reload:
            if mod in sys.modules:
                del sys.modules[mod]

        # Reimport generator
        from generator import DynamicHackforgeGenerator

        # Create new generator instance (will auto-discover new blueprint)
        gen = DynamicHackforgeGenerator(core_dir=str(CORE_PATH))

        # Find the blueprint we just created
        blueprint_id = None
        for bp_id, bp in gen.blueprints.items():
            if bp.category == category:
                blueprint_id = bp_id
                logger.info(f"Found blueprint: {bp.name} ({bp_id})")
                break

        if not blueprint_id:
            logger.error(f"Available blueprints: {list(gen.blueprints.keys())}")
            logger.error(f"Looking for category: {category}")
            raise HTTPException(
                status_code=500,
                detail=f"Blueprint not found after generation. Category: {category}. Available: {list(gen.blueprints.keys())}"
            )

        # STEP 3: Generate ONLY ONE machine using generate_single_machine()
        logger.info(f"\nSTEP 3: Generating single machine for {category}...")

        machine = gen.generate_single_machine(
            blueprint_id=blueprint_id,
            difficulty=2,  # Default medium difficulty
            user_id="api_generated"
        )

        if not machine:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate machine config"
            )

        logger.info(f"✓ Generated and exported machine: {machine.machine_id}")

        # STEP 4: Generate Docker application using template_engine
        logger.info("\nSTEP 4: Generating Docker application...")

        # Remove cached template_engine module
        if 'template_engine' in sys.modules:
            del sys.modules['template_engine']

        from template_engine import TemplateEngine
        import inspect

        template_engine_instance = TemplateEngine(
            machines_dir=str(CORE_PATH / "generated_machines")
        )

        machine_dir = CORE_PATH / "generated_machines" / machine.machine_id

        # Find available port starting from 8080
        import socket
        
        def find_available_port(start_port=8080, max_attempts=100):
            """Find an available port starting from start_port"""
            for port in range(start_port, start_port + max_attempts):
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.bind(('', port))
                        return port
                except OSError:
                    continue
            return start_port
        
        port = find_available_port()
        logger.info(f"Using port: {port}")

        # Inspect the method signature to determine how to call it
        try:
            sig = inspect.signature(template_engine_instance.generate_machine_app)
            params = list(sig.parameters.keys())
            logger.info(f"Template engine signature: generate_machine_app({', '.join(params)})")
        except Exception as e:
            logger.warning(f"Could not inspect signature: {e}")
            params = []

        # Try different calling conventions based on the signature
        result = None
        last_error = None

        # Strategy 1: All positional arguments (most common)
        if not result:
            try:
                logger.info("Attempting: generate_machine_app(machine, machine_dir, port) - all positional")
                result = template_engine_instance.generate_machine_app(machine, machine_dir, port)
                logger.info(f"✓ SUCCESS with all positional arguments")
            except Exception as e:
                last_error = e
                logger.warning(f"Strategy 1 failed: {e}")

        # Strategy 2: Machine positional, rest keyword
        if not result:
            try:
                logger.info("Attempting: generate_machine_app(machine, machine_dir=..., port=...)")
                result = template_engine_instance.generate_machine_app(machine, machine_dir=machine_dir, port=port)
                logger.info(f"✓ SUCCESS with machine positional, rest keyword")
            except Exception as e:
                last_error = e
                logger.warning(f"Strategy 2 failed: {e}")

        # Strategy 3: All keyword arguments
        if not result:
            try:
                logger.info("Attempting: generate_machine_app(machine=..., machine_dir=..., port=...)")
                result = template_engine_instance.generate_machine_app(machine=machine, machine_dir=machine_dir, port=port)
                logger.info(f"✓ SUCCESS with all keyword arguments")
            except Exception as e:
                last_error = e
                logger.warning(f"Strategy 3 failed: {e}")

        # Strategy 4: Only machine and machine_dir (no port) - OLD SIGNATURE
        if not result:
            try:
                logger.info("Attempting: generate_machine_app(machine, machine_dir) - no port (old signature)")
                result = template_engine_instance.generate_machine_app(machine, machine_dir)
                logger.info(f"✓ SUCCESS with old signature (no port)")
                logger.warning("Note: Template engine doesn't use port parameter - you may need to update it")
            except Exception as e:
                last_error = e
                logger.warning(f"Strategy 4 failed: {e}")

        # Strategy 5: Try with dictionary unpacking
        if not result:
            try:
                logger.info("Attempting: generate_machine_app(**kwargs)")
                kwargs = {'machine': machine, 'machine_dir': machine_dir, 'port': port}
                result = template_engine_instance.generate_machine_app(**kwargs)
                logger.info(f"✓ SUCCESS with dictionary unpacking")
            except Exception as e:
                last_error = e
                logger.warning(f"Strategy 5 failed: {e}")

        # If all strategies failed, raise detailed error
        if not result:
            error_details = f"""
Failed to call template_engine.generate_machine_app() with all strategies.

Last error: {last_error}

Attempted strategies:
1. All positional: generate_machine_app(machine, machine_dir, port)
2. Mixed: generate_machine_app(machine, machine_dir=..., port=...)
3. All keyword: generate_machine_app(machine=..., machine_dir=..., port=...)
4. Old signature: generate_machine_app(machine, machine_dir)
5. Dictionary unpacking: generate_machine_app(**kwargs)

Please check your template_engine.py file and verify the generate_machine_app() method signature.
Expected: def generate_machine_app(self, machine, machine_dir, port)
"""
            logger.error(error_details)
            raise HTTPException(
                status_code=500,
                detail=f"Template engine compatibility error: {str(last_error)}"
            )

        logger.info(f"✓ Generated Docker app successfully")


        # STEP 5: Generate docker-compose.yml for this single machine
        logger.info("\nSTEP 5: Generating docker-compose.yml...")

        # Get infrastructure requirements from config
        needs_database = config_data.get('infrastructure', {}).get('needs_database', False)
        database_type = config_data.get('infrastructure', {}).get('database_type', 'mysql')

        # Get flag location from config
        flag_location = machine.flag.get('location', '/var/www/html/flag.txt')
        flag_location = flag_location.replace(':', '_').replace('//', '/')
        if not flag_location.startswith('/'):
            flag_location = '/' + flag_location

        # Build docker-compose based on infrastructure needs
        if needs_database:
            compose_content = f"""version: '3.8'

services:
  {machine.machine_id}:
    build: .
    container_name: hackforge_{machine.machine_id}
    ports:
      - "{port}:80"
    volumes:
      - ./app:/var/www/html
      - ./flag.txt:{flag_location}:ro
    environment:
      - MACHINE_ID={machine.machine_id}
      - FLAG_LOCATION={flag_location}
      - DB_HOST=db
      - DB_USER=hackforge
      - DB_PASSWORD=hackforge123
      - DB_NAME=hackforge
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: {database_type}:latest
    container_name: hackforge_{machine.machine_id}_db
    environment:
      - MYSQL_ROOT_PASSWORD=root123
      - MYSQL_DATABASE=hackforge
      - MYSQL_USER=hackforge
      - MYSQL_PASSWORD=hackforge123
    volumes:
      - db_data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    restart: unless-stopped

volumes:
  db_data:
"""
        else:
            compose_content = f"""version: '3.8'

services:
  {machine.machine_id}:
    build: .
    container_name: hackforge_{machine.machine_id}
    ports:
      - "{port}:80"
    volumes:
      - ./app:/var/www/html
      - ./flag.txt:{flag_location}:ro
    environment:
      - MACHINE_ID={machine.machine_id}
      - FLAG_LOCATION={flag_location}
    restart: unless-stopped
"""

        compose_file = machine_dir / "docker-compose.yml"
        with open(compose_file, 'w') as f:
            f.write(compose_content)

        logger.info(f"✓ Generated: {compose_file}")

        # STEP 5.5: Generate init.sql if database is needed
        if needs_database and config_data.get('database_schema'):
            logger.info("\nSTEP 5.5: Generating database initialization script...")

            db_schema = config_data['database_schema']
            init_sql_content = "-- Auto-generated database initialization\n\n"

            # Create tables
            for table in db_schema.get('tables', []):
                table_name = table['name']
                columns = ', '.join(table['columns'])
                init_sql_content += f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});\n\n"

            # Insert seed data
            seed_data = db_schema.get('seed_data', {})
            for table_name, rows in seed_data.items():
                for row in rows:
                    columns = ', '.join(row.keys())
                    values = []
                    for value in row.values():
                        if value == 'NOW()':
                            values.append('NOW()')
                        elif value == '{{FLAG}}':
                            values.append(f"'{machine.flag['content']}'")
                        else:
                            # Escape single quotes in values
                            escaped_value = str(value).replace("'", "\\'")
                            values.append(f"'{escaped_value}'")
                    values_str = ', '.join(values)
                    init_sql_content += f"INSERT INTO {table_name} ({columns}) VALUES ({values_str});\n"

            init_sql_file = machine_dir / "init.sql"
            with open(init_sql_file, 'w') as f:
                f.write(init_sql_content)

            logger.info(f"✓ Generated: {init_sql_file}")

        # STEP 6: Start Docker container automatically
        logger.info("\nSTEP 6: Starting Docker container...")

        container_started = False
        container_url = None

        try:
            result = subprocess.run(
                ["docker-compose", "up", "-d", "--build"],
                cwd=str(machine_dir),
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                logger.info("✓ Docker container started successfully")
                container_started = True
                container_url = f"http://4.231.90.52:{port}"

                # Wait a moment for container to fully start
                time.sleep(2)
            else:
                logger.warning(f"Container start failed: {result.stderr}")

        except Exception as e:
            logger.warning(f"Could not start container: {e}")

        logger.info("\n" + "="*60)
        logger.info("✓ PIPELINE COMPLETE!")
        logger.info("="*60)

        return {
            "success": True,
            "message": "Machine generated and ready!",
            "category": category,
            "machine_id": machine.machine_id,
            "variant": machine.variant,
            "difficulty": machine.difficulty,
            "flag": machine.flag['content'],
            "directory": str(machine_dir),
            "port": port,
            "infrastructure": config_data.get('infrastructure'),
            "has_database": needs_database,
            "files_generated": {
                "blueprint": f"blueprints/{category}_blueprint.yaml",
                "mutation": f"mutations/{category}_mutation.py",
                "template": f"templates/{category}_templates.py",
                "machine_config": f"generated_machines/{machine.machine_id}/config.json",
                "docker_app": f"generated_machines/{machine.machine_id}/app/index.php",
                "dockerfile": f"generated_machines/{machine.machine_id}/Dockerfile",
                "compose": f"generated_machines/{machine.machine_id}/docker-compose.yml",
                "init_sql": f"generated_machines/{machine.machine_id}/init.sql" if needs_database else None
            },
            "container_started": container_started,
            "url": container_url,
            "next_steps": [
                f"Access machine at: {container_url}" if container_started else f"Start container: cd generated_machines/{machine.machine_id} && docker-compose up -d",
                "Test the vulnerability",
                "Submit flag via /machines page"
            ]
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")

@app.get("/api/configs")
async def list_configs():
    """List all vulnerability configs"""
    try:
        configs_dir = CORE_PATH / "configs"

        if not configs_dir.exists():
            logger.warning(f"Configs directory not found: {configs_dir}")
            return []

        config_files = list(configs_dir.glob("*.json"))
        logger.info(f"Found {len(config_files)} config files in {configs_dir}")

        configs = []
        for config_file in config_files:
            try:
                with open(config_file, 'r') as f:
                    config_data = json.load(f)

                # Extract relevant info
                configs.append({
                    'filename': config_file.name,
                    'category': config_data.get('category', 'unknown'),
                    'name': config_data.get('name', 'Unknown'),
                    'vulnerability_id': config_data.get('vulnerability_id', 'unknown'),
                    'description': config_data.get('description', ''),
                    'difficulty_range': config_data.get('difficulty_range', [1, 5]),
                    'variants': config_data.get('variants', []),
                    'variants_count': len(config_data.get('variants', [])),
                    'path': str(config_file)
                })

                logger.info(f"✓ Loaded config: {config_data.get('name')}")

            except Exception as e:
                logger.error(f"✗ Failed to load {config_file.name}: {e}")

        logger.info(f"Returning {len(configs)} configs to frontend")
        return configs

    except Exception as e:
        logger.error(f"Error in list_configs: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/configs/{category}")
async def get_config(category: str):
    """Get specific config details"""
    try:
        configs_dir = CORE_PATH / "configs"
        config_path = configs_dir / f"{category}.json"

        if not config_path.exists():
            raise HTTPException(status_code=404, detail=f"Config not found: {category}")

        with open(config_path, 'r') as f:
            config_data = json.load(f)

        return {
            'filename': config_path.name,
            'path': str(config_path),
            'config': config_data
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting config {category}: {e}")
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/api/configs")
async def create_config_and_generate(config: VulnerabilityConfig, auto_generate: bool = True):
    """
    Create config and optionally auto-generate everything
    UPDATED: Handles new config format with infrastructure and database_schema

    Parameters:
    - config: VulnerabilityConfig object with new format
    - auto_generate: If True, runs full pipeline automatically (default: True)
    """
    try:
        # Create configs directory if needed
        configs_dir = CORE_PATH / "configs"
        configs_dir.mkdir(exist_ok=True)

        # Save config file
        config_filename = f"{config.category}.json"
        config_path = configs_dir / config_filename

        config_data = config.dict()

        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=2)

        logger.info(f"✓ Created config: {config_path}")
        logger.info(f"  - Needs database: {config_data.get('infrastructure', {}).get('needs_database', False)}")
        logger.info(f"  - Database type: {config_data.get('infrastructure', {}).get('database_type', 'N/A')}")

        response = {
            "message": "Config created successfully",
            "config_file": config_filename,
            "path": str(config_path),
            "config": config_data,
            "infrastructure": config_data.get('infrastructure')
        }

        # If auto_generate is True, run the full pipeline
        if auto_generate:
            logger.info("\n🚀 Auto-generating machine from config...")

            try:
                # Run the full pipeline
                pipeline_result = await generate_machine_from_config(config.category, BackgroundTasks())

                response["auto_generated"] = True
                response["machine"] = pipeline_result
                response["message"] = "Config created and machine generated successfully!"

            except Exception as e:
                logger.error(f"Auto-generation failed: {e}")
                response["auto_generated"] = False
                response["auto_generate_error"] = str(e)
                response["message"] = "Config created, but auto-generation failed. You can generate manually."

        return response

    except Exception as e:
        logger.error(f"Failed to create config: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create config: {str(e)}")

# Keep the original simple generate endpoint for backward compatibility
@app.post("/api/configs/{category}/generate")
async def generate_from_config(category: str, background_tasks: BackgroundTasks):
    """
    Generate ONLY blueprint/mutation/template (original behavior)
    Does NOT generate machine or Docker app
    """
    try:
        configs_dir = CORE_PATH / "configs"
        config_path = configs_dir / f"{category}.json"

        if not config_path.exists():
            raise HTTPException(status_code=404, detail=f"Config not found: {category}")

        logger.info(f"Generating components from config: {category}")

        sys.path.insert(0, str(CORE_PATH))
        from vuln_generator import VulnerabilityGenerator

        generator = VulnerabilityGenerator(str(config_path))
        generator.generate_all(str(CORE_PATH))

        logger.info(f"✓ Generated all components for {category}")

        return {
            "message": "Blueprint, mutation, and template generated successfully",
            "category": category,
            "files_created": {
                "blueprint": f"blueprints/{category}_blueprint.yaml",
                "mutation": f"mutations/{category}_mutation.py",
                "template": f"templates/{category}_templates.py"
            },
            "next_step": f"Generate machine with: POST /api/configs/{category}/generate-machine"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to generate from config: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


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
