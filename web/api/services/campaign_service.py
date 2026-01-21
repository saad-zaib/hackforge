import logging
import time
from pathlib import Path
from dependencies import generator, template_engine, get_database

logger = logging.getLogger(__name__)

class CampaignService:
    @staticmethod
    def create_campaign(user_id: str, campaign_name: str, difficulty: int, count: int = None):
        """Create a new campaign with all machines"""
        logger.info(f"Creating campaign: {campaign_name}")
        
        # Get database instance
        db = get_database()
        if not db:
            raise Exception("Database not available")

        # Generate machines
        machines = generator.generate_campaign(
            user_id=user_id,
            difficulty=difficulty,
            count=count
        )

        if not machines:
            raise ValueError("No machines generated")

        # Create campaign directory
        campaign_id = f"campaign_{int(time.time())}"
        campaign_output_dir = f"campaigns/{campaign_id}"

        # Export campaign
        campaign_path = generator.export_campaign(machines, output_dir=campaign_output_dir)

        # Generate Docker apps
        machine_infos = template_engine.generate_campaign_apps(campaign_path)

        # Prepare campaign data
        campaign_data = {
            'campaign_id': campaign_id,
            'campaign_name': campaign_name,
            'user_id': user_id,
            'difficulty': difficulty,
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
        db.create_campaign(campaign_data)

        # Create progress records
        for machine in machines:
            progress_data = {
                'user_id': user_id,
                'machine_id': machine.machine_id,
                'campaign_id': campaign_id
            }
            db.create_progress(progress_data)

        return campaign_data, campaign_path
