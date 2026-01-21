import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

class DockerService:
    @staticmethod
    def start_campaign_containers(campaign_path: Path):
        """Start Docker containers for a campaign"""
        try:
            compose_file = campaign_path / "docker-compose.yml"
            
            if not compose_file.exists():
                logger.warning(f"No docker-compose.yml found in {campaign_path}")
                return False
            
            logger.info(f"Starting containers for {campaign_path.name}...")
            
            result = subprocess.run(
                ["docker-compose", "up", "-d", "--build"],
                cwd=str(campaign_path),
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                logger.info("✓ Containers started successfully")
                return True
            else:
                logger.error(f"✗ Failed to start containers: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error starting containers: {e}")
            return False
