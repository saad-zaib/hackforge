#!/usr/bin/env python3
"""
Campaign Migration Script
Imports existing campaigns from filesystem into MongoDB
"""

import sys
import json
from pathlib import Path

# Add paths
sys.path.append(str(Path(__file__).parent.parent / "database"))
sys.path.append(str(Path(__file__).parent.parent.parent / "core"))

try:
    from database import get_db
    
    print("=" * 60)
    print("HACKFORGE CAMPAIGN MIGRATION")
    print("Importing existing campaigns into MongoDB")
    print("=" * 60)
    print()
    
    # Get database instance
    db = get_db()
    print("✓ Connected to MongoDB")
    
    # Find campaigns directory (FIXED PATH)
    campaigns_dir = Path(__file__).parent.parent.parent / "core" / "campaigns"
    
    if not campaigns_dir.exists():
        print(f"✗ Campaigns directory not found: {campaigns_dir}")
        print(f"\nExpected location: {campaigns_dir}")
        print(f"Create campaigns first using the web interface or './hackforge generate'")
        sys.exit(1)
    
    print(f"✓ Found campaigns directory: {campaigns_dir}")
    print()
    
    # Find all campaign directories
    campaign_dirs = [d for d in campaigns_dir.iterdir() if d.is_dir() and d.name.startswith('campaign_')]
    
    print(f"Found {len(campaign_dirs)} campaign(s) on filesystem")
    print()
    
    if len(campaign_dirs) == 0:
        print("No campaigns to import!")
        sys.exit(0)
    
    imported = 0
    skipped = 0
    errors = 0
    
    for camp_dir in sorted(campaign_dirs):
        campaign_id = camp_dir.name
        manifest_file = camp_dir / "campaign.json"
        
        print(f"Processing: {campaign_id}")
        
        # Check if already in database
        existing = db.get_campaign(campaign_id)
        if existing:
            print(f"  ⊘ Already in database, skipping")
            skipped += 1
            continue
        
        # Read manifest
        if not manifest_file.exists():
            print(f"  ✗ No campaign.json found, skipping")
            errors += 1
            continue
        
        try:
            with open(manifest_file, 'r') as f:
                manifest = json.load(f)
            
            # Extract campaign info
            machines = manifest.get('machines', [])
            
            # Determine difficulty (use average of machines)
            difficulties = [m.get('difficulty', 2) for m in machines]
            avg_difficulty = sum(difficulties) // len(difficulties) if difficulties else 2
            
            # Create campaign data for database
            campaign_data = {
                'campaign_id': campaign_id,
                'campaign_name': f"Imported Campaign {campaign_id.split('_')[1]}",  # Default name
                'user_id': 'user_default',  # Default user
                'difficulty': avg_difficulty,
                'machine_count': len(machines),
                'status': 'active',
                'machines': [
                    {
                        'machine_id': m['machine_id'],
                        'variant': m['variant'],
                        'difficulty': m['difficulty'],
                        'blueprint_id': m['blueprint_id'],
                        'flag': m['flag']['content'],
                        'port': None  # Will be assigned by template engine
                    }
                    for m in machines
                ]
            }
            
            # Save to database
            db.create_campaign(campaign_data)
            
            # Create progress records for each machine
            for machine in machines:
                progress_data = {
                    'user_id': 'user_default',
                    'machine_id': machine['machine_id'],
                    'campaign_id': campaign_id
                }
                try:
                    db.create_progress(progress_data)
                except Exception:
                    pass  # Progress might already exist
            
            print(f"  ✓ Imported: {len(machines)} machines, difficulty {avg_difficulty}")
            imported += 1
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
            errors += 1
            continue
    
    print()
    print("=" * 60)
    print("MIGRATION SUMMARY")
    print("=" * 60)
    print(f"  Imported: {imported}")
    print(f"  Skipped (already in DB): {skipped}")
    print(f"  Errors: {errors}")
    print()
    
    if imported > 0:
        print("✓ Migration completed successfully!")
        print("\nYou can now:")
        print("  1. Refresh your browser")
        print("  2. View campaigns in 'My Campaigns'")
        print("  3. Click on any campaign to manage it")
    else:
        print("⊘ No new campaigns were imported")
    
    print("=" * 60)
    
except ImportError as e:
    print(f"✗ Failed to import required modules: {e}")
    print("\nMake sure you're running from the correct directory:")
    print("  cd ~/hackforge/web/api")
    sys.exit(1)
except Exception as e:
    print(f"✗ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
