"""
Hackforge Web API
FastAPI REST API for managing campaigns and machines
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sys
import os
from pathlib import Path
import json
import time

# Add parent directories to path
sys.path.append(str(Path(__file__).parent.parent.parent / "core"))
sys.path.append(str(Path(__file__).parent.parent.parent / "docker" / "orchestrator"))

from generator import HackforgeGenerator
from template_engine import TemplateEngine
from orchestrator import DockerOrchestrator
from base import MachineConfig

# Initialize FastAPI
app = FastAPI(
    title="Hackforge API",
    description="REST API for Dynamic Vulnerability Training Platform",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
generator = HackforgeGenerator()
template_engine = TemplateEngine()
orchestrator = DockerOrchestrator()


# ============================================================================
# Pydantic Models
# ============================================================================

class CampaignCreateRequest(BaseModel):
    user_id: str
    difficulty: int = 2
    count: Optional[int] = None

class CampaignResponse(BaseModel):
    campaign_id: str
    user_id: str
    difficulty: int
    machines: List[Dict]
    created_at: str
    status: str

class MachineResponse(BaseModel):
    machine_id: str
    variant: str
    difficulty: int
    blueprint_id: str
    flag: str
    port: Optional[int] = None
    url: Optional[str] = None
    status: Optional[str] = None

class FlagSubmitRequest(BaseModel):
    machine_id: str
    flag: str
    user_id: str

class FlagValidationResponse(BaseModel):
    correct: bool
    message: str
    points: Optional[int] = None


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "Hackforge API",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "blueprints": "/api/blueprints",
            "campaigns": "/api/campaigns",
            "machines": "/api/machines",
            "docker": "/api/docker"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time()
    }


# ============================================================================
# Blueprint Endpoints
# ============================================================================

@app.get("/api/blueprints", response_model=List[Dict])
async def list_blueprints():
    """List all available vulnerability blueprints"""
    blueprints = generator.list_blueprints()
    
    return [
        {
            "blueprint_id": bp.blueprint_id,
            "name": bp.name,
            "category": bp.category,
            "difficulty_range": bp.difficulty_range,
            "variants": bp.variants,
            "description": bp.description
        }
        for bp in blueprints
    ]

@app.get("/api/blueprints/{blueprint_id}")
async def get_blueprint(blueprint_id: str):
    """Get specific blueprint details"""
    blueprint = generator.get_blueprint(blueprint_id)
    
    if not blueprint:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    
    return blueprint.to_dict()


# ============================================================================
# Campaign Endpoints
# ============================================================================

@app.post("/api/campaigns", response_model=CampaignResponse)
async def create_campaign(request: CampaignCreateRequest, background_tasks: BackgroundTasks):
    """
    Create a new campaign with vulnerable machines
    This generates configs, templates, and optionally deploys containers
    """
    
    # Validate difficulty
    if not 1 <= request.difficulty <= 5:
        raise HTTPException(status_code=400, detail="Difficulty must be between 1 and 5")
    
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
    
    # Generate applications from configs
    machine_infos = template_engine.generate_campaign_apps(campaign_path)
    
    # Get campaign data
    campaign_file = Path(campaign_path) / "campaign.json"
    with open(campaign_file, 'r') as f:
        campaign_data = json.load(f)
    
    campaign_id = Path(campaign_path).name
    
    # Add deployment info to machines
    for i, machine_info in enumerate(machine_infos):
        machines[i].metadata['port'] = machine_info['port']
        machines[i].metadata['url'] = f"http://localhost:{machine_info['port']}"
    
    response = CampaignResponse(
        campaign_id=campaign_id,
        user_id=request.user_id,
        difficulty=request.difficulty,
        machines=[
            {
                "machine_id": m.machine_id,
                "variant": m.variant,
                "difficulty": m.difficulty,
                "blueprint_id": m.blueprint_id,
                "flag": m.flag['content'],
                "port": m.metadata.get('port'),
                "url": m.metadata.get('url')
            }
            for m in machines
        ],
        created_at=campaign_data['created_at'],
        status="ready"
    )
    
    return response

@app.get("/api/campaigns")
async def list_campaigns():
    """List all campaigns"""
    campaigns_dir = Path(__file__).parent.parent.parent / "core" / "campaigns"
    
    if not campaigns_dir.exists():
        return []
    
    campaigns = []
    
    for campaign_dir in campaigns_dir.glob("campaign_*"):
        campaign_file = campaign_dir / "campaign.json"
        
        if campaign_file.exists():
            with open(campaign_file, 'r') as f:
                data = json.load(f)
            
            campaigns.append({
                "campaign_id": campaign_dir.name,
                "created_at": data.get('created_at'),
                "total_machines": data.get('total_machines'),
                "machines": [
                    {
                        "machine_id": m['machine_id'],
                        "variant": m['variant'],
                        "difficulty": m['difficulty']
                    }
                    for m in data.get('machines', [])
                ]
            })
    
    return campaigns

@app.get("/api/campaigns/{campaign_id}")
async def get_campaign(campaign_id: str):
    """Get specific campaign details"""
    campaigns_dir = Path(__file__).parent.parent.parent / "core" / "campaigns"
    campaign_path = campaigns_dir / campaign_id
    campaign_file = campaign_path / "campaign.json"
    
    if not campaign_file.exists():
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    with open(campaign_file, 'r') as f:
        data = json.load(f)
    
    return data

@app.delete("/api/campaigns/{campaign_id}")
async def delete_campaign(campaign_id: str):
    """Delete a campaign"""
    campaigns_dir = Path(__file__).parent.parent.parent / "core" / "campaigns"
    campaign_path = campaigns_dir / campaign_id
    
    if not campaign_path.exists():
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    import shutil
    shutil.rmtree(campaign_path)
    
    return {"message": "Campaign deleted successfully"}


# ============================================================================
# Machine Endpoints
# ============================================================================

@app.get("/api/machines", response_model=List[MachineResponse])
async def list_machines():
    """List all generated machines"""
    machines = orchestrator.list_machines()
    
    return [
        MachineResponse(
            machine_id=m['machine_id'],
            variant=m['variant'],
            difficulty=m['difficulty'],
            blueprint_id=m['blueprint_id'],
            flag=m['flag']
        )
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


# ============================================================================
# Flag Validation Endpoints
# ============================================================================

@app.post("/api/flags/validate", response_model=FlagValidationResponse)
async def validate_flag(request: FlagSubmitRequest):
    """Validate a submitted flag"""
    
    # Find machine
    machines = orchestrator.list_machines()
    target_machine = None
    
    for machine in machines:
        if machine['machine_id'] == request.machine_id:
            target_machine = machine
            break
    
    if not target_machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    # Validate flag
    correct = request.flag.strip() == target_machine['flag'].strip()
    
    if correct:
        # Calculate points based on difficulty
        points = target_machine['difficulty'] * 100
        
        return FlagValidationResponse(
            correct=True,
            message="🎉 Correct! Flag captured successfully!",
            points=points
        )
    else:
        return FlagValidationResponse(
            correct=False,
            message="❌ Incorrect flag. Try again!",
            points=0
        )


# ============================================================================
# Docker Management Endpoints
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
# Statistics Endpoints
# ============================================================================

@app.get("/api/stats")
async def get_statistics():
    """Get overall platform statistics"""
    
    blueprints = generator.list_blueprints()
    machines = orchestrator.list_machines()
    
    campaigns_dir = Path(__file__).parent.parent.parent / "core" / "campaigns"
    total_campaigns = len(list(campaigns_dir.glob("campaign_*"))) if campaigns_dir.exists() else 0
    
    return {
        "total_blueprints": len(blueprints),
        "total_machines": len(machines),
        "total_campaigns": total_campaigns,
        "vulnerability_types": [bp.category for bp in blueprints],
        "difficulty_distribution": {
            1: sum(1 for m in machines if m['difficulty'] == 1),
            2: sum(1 for m in machines if m['difficulty'] == 2),
            3: sum(1 for m in machines if m['difficulty'] == 3),
            4: sum(1 for m in machines if m['difficulty'] == 4),
            5: sum(1 for m in machines if m['difficulty'] == 5),
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║                 HACKFORGE WEB API                         ║
╚═══════════════════════════════════════════════════════════╝

Starting API server...
    """)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
