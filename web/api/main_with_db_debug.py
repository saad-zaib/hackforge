"""
Enhanced API with Debug Logging
Add this to see what's happening during campaign creation
"""

# Add this at the top of your main_with_db.py after imports
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Then modify the create_campaign endpoint to include detailed logging:

@app.post("/api/campaigns")
async def create_campaign(request: CampaignCreateRequest, background_tasks: BackgroundTasks):
    """Create a new campaign with database tracking and detailed logging"""
    
    logger.info(f"=" * 60)
    logger.info(f"CREATING CAMPAIGN")
    logger.info(f"User: {request.user_id}")
    logger.info(f"Name: {request.campaign_name}")
    logger.info(f"Difficulty: {request.difficulty}")
    logger.info(f"Count: {request.count}")
    logger.info(f"=" * 60)

    # Validate difficulty
    if not 1 <= request.difficulty <= 5:
        logger.error(f"Invalid difficulty: {request.difficulty}")
        raise HTTPException(status_code=400, detail="Difficulty must be between 1 and 5")
    
    # Validate campaign name
    if not request.campaign_name or len(request.campaign_name.strip()) == 0:
        logger.error("Campaign name is empty")
        raise HTTPException(status_code=400, detail="Campaign name is required")

    # Check if user exists, create if not
    logger.info("Checking user...")
    user = db.get_user(request.user_id)
    if not user:
        logger.info("User not found, creating...")
        user_data = {
            'user_id': request.user_id,
            'username': request.user_id,
            'email': f"{request.user_id}@hackforge.local",
            'role': 'student'
        }
        db.create_user(user_data)
        logger.info("✓ User created")
    else:
        logger.info("✓ User exists")

    # Generate campaign
    logger.info("Generating campaign machines...")
    try:
        machines = generator.generate_campaign(
            user_id=request.user_id,
            difficulty=request.difficulty,
            count=request.count
        )
        logger.info(f"✓ Generated {len(machines)} machines")
    except Exception as e:
        logger.error(f"Failed to generate campaign: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate campaign: {str(e)}")

    if not machines:
        logger.error("No machines generated")
        raise HTTPException(status_code=500, detail="Failed to generate campaign")

    # Export campaign
    logger.info("Exporting campaign to filesystem...")
    try:
        campaign_path = generator.export_campaign(machines)
        campaign_id = Path(campaign_path).name
        logger.info(f"✓ Exported to: {campaign_path}")
        logger.info(f"✓ Campaign ID: {campaign_id}")
    except Exception as e:
        logger.error(f"Failed to export campaign: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to export campaign: {str(e)}")

    # Generate applications
    logger.info("Generating Docker applications...")
    try:
        machine_infos = template_engine.generate_campaign_apps(campaign_path)
        logger.info(f"✓ Generated {len(machine_infos)} Docker apps")
    except Exception as e:
        logger.error(f"Failed to generate apps: {e}")
        machine_infos = []

    # Prepare campaign data for database
    logger.info("Preparing campaign data for database...")
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
    
    logger.info(f"Campaign data prepared:")
    logger.info(f"  - ID: {campaign_data['campaign_id']}")
    logger.info(f"  - Name: {campaign_data['campaign_name']}")
    logger.info(f"  - Machines: {campaign_data['machine_count']}")

    # Save to database
    logger.info("Saving campaign to MongoDB...")
    try:
        db.create_campaign(campaign_data)
        logger.info("✓ Campaign saved to database")
    except Exception as e:
        logger.error(f"✗ FAILED TO SAVE TO DATABASE: {e}")
        import traceback
        logger.error(traceback.format_exc())
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
            logger.warning(f"Failed to create progress for {machine.machine_id}: {e}")

    logger.info("✓ Campaign creation completed successfully!")
    logger.info("=" * 60)

    return {
        'campaign_id': campaign_id,
        'campaign_name': request.campaign_name,
        'user_id': request.user_id,
        'difficulty': request.difficulty,
        'machines': campaign_data['machines'],
        'status': 'created'
    }

