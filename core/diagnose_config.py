#!/usr/bin/env python3
"""
Diagnostic: Check config.json structure
"""

import json
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python3 diagnose_config.py <machine_dir>")
    sys.exit(1)

machine_dir = Path(sys.argv[1])
config_file = machine_dir / "config.json"

if not config_file.exists():
    print(f"❌ Config file not found: {config_file}")
    sys.exit(1)

print(f"📋 Analyzing: {config_file}\n")
print("="*60)

with open(config_file, 'r') as f:
    config = json.load(f)

# Check top-level structure
print("TOP-LEVEL KEYS:")
for key in config.keys():
    print(f"  ✓ {key}")

print("\n" + "="*60)

# Check blueprint_config
blueprint_config = config.get('blueprint_config', {})
if blueprint_config:
    print("BLUEPRINT_CONFIG:")
    print(f"  Size: {len(json.dumps(blueprint_config))} bytes")
    print(f"  Keys: {list(blueprint_config.keys())}")
    
    # Check critical fields
    category = blueprint_config.get('category')
    print(f"\n  category: {category}")
    
    infrastructure = blueprint_config.get('infrastructure', {})
    if infrastructure:
        print(f"  infrastructure.needs_database: {infrastructure.get('needs_database')}")
        print(f"  infrastructure.database_type: {infrastructure.get('database_type')}")
    else:
        print(f"  ❌ infrastructure: NOT FOUND")
else:
    print("❌ blueprint_config: EMPTY OR MISSING")

print("\n" + "="*60)

# Check metadata
metadata = config.get('metadata', {})
category_in_metadata = metadata.get('category')
print(f"metadata.category: {category_in_metadata}")

# Check blueprint_id
blueprint_id = config.get('blueprint_id')
print(f"blueprint_id: {blueprint_id}")

print("\n" + "="*60)
print("DIAGNOSIS:")

if blueprint_config and blueprint_config.get('category'):
    print("✅ Config looks good - category found in blueprint_config")
elif category_in_metadata:
    print("⚠️  Category only in metadata, not in blueprint_config")
    print("   This might cause docker-compose issues")
elif blueprint_id:
    category_from_id = blueprint_id.split('_')[0]
    print(f"⚠️  No category in blueprint_config, extracting from blueprint_id: {category_from_id}")
else:
    print("❌ No way to determine category!")

print("="*60)
