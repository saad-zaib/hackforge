from fastapi import APIRouter, HTTPException, Depends
from dependencies import get_database, orchestrator
import logging
import json
from pathlib import Path

router = APIRouter(prefix="/api/machines", tags=["machines"])
logger = logging.getLogger(__name__)

def require_db():
    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    return db

@router.get("")
async def list_machines(db=Depends(require_db)):
    """List all machines with enhanced metadata"""
    try:
        machines = orchestrator.list_machines()
        enriched_machines = []

        for machine in machines:
            machine_id = machine['machine_id']

            # Find campaign
            campaign = db.campaigns.find_one({'machines.machine_id': machine_id})
            
            # Get progress
            progress = db.progress.find_one({'machine_id': machine_id})

            # Get Docker info
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
                            'ports': container.ports
                        }
                        break
            except Exception as e:
                logger.warning(f"Could not get Docker info for {machine_id}: {e}")
                container_info = None

            enriched_machine = {
                'machine_id': machine['machine_id'],
                'variant': machine['variant'],
                'difficulty': machine['difficulty'],
                'blueprint_id': machine['blueprint_id'],
                'flag': machine['flag'],
                'directory': machine['directory'],
                'campaign_id': campaign['campaign_id'] if campaign else None,
                'campaign_name': campaign.get('campaign_name', 'Unknown') if campaign else None,
                'solved': progress.get('solved', False) if progress else False,
                'attempts': progress.get('attempts', 0) if progress else 0,
                'points_earned': progress.get('points_earned', 0) if progress else 0,
                'container': container_info,
                'is_running': container_info['status'] == 'running' if container_info else False,
                'url': None
            }

            # Extract URL
            if container_info and container_info['status'] == 'running':
                ports = container_info.get('ports', {})
                for container_port, host_bindings in ports.items():
                    if host_bindings:
                        host_port = host_bindings[0]['HostPort']
                        enriched_machine['url'] = f"http://localhost:{host_port}"
                        break

            enriched_machines.append(enriched_machine)

        return enriched_machines

    except Exception as e:
        logger.error(f"Error listing machines: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{machine_id}")
async def get_machine(machine_id: str, db=Depends(require_db)):
    """Get specific machine details"""
    try:
        machines = orchestrator.list_machines()
        machine = next((m for m in machines if m['machine_id'] == machine_id), None)

        if not machine:
            raise HTTPException(status_code=404, detail="Machine not found")

        # Load config
        config_file = Path(machine['directory']) / "config.json"
        with open(config_file, 'r') as f:
            config = json.load(f)

        # Get campaign and progress
        campaign = db.campaigns.find_one({'machines.machine_id': machine_id})
        progress = db.progress.find_one({'machine_id': machine_id})

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

@router.get("/{machine_id}/stats")
async def get_machine_statistics(machine_id: str, db=Depends(require_db)):
    """Get statistics for a specific machine"""
    try:
        stats = db.get_machine_stats(machine_id)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
