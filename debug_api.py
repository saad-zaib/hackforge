#!/usr/bin/env python3
import json, docker
from pathlib import Path

core = Path.cwd() / "core"
gen = core / "generated_machines"

# Get containers
client = docker.from_env()
containers = {c.name.replace('hackforge_', ''): {'id': c.id[:12], 'status': c.status} 
              for c in client.containers.list(all=True) if 'hackforge_' in c.name}

print(f"Containers: {list(containers.keys())}")

# Get machines
machines = []
for d in gen.iterdir():
    if not d.is_dir(): continue
    cfg = d / "config.json"
    if not cfg.exists(): continue
    
    with open(cfg) as f:
        data = json.load(f)
    
    mid = data['machine_id']
    machines.append({
        'machine_id': mid,
        'variant': data.get('variant', 'Unknown'),
        'difficulty': data.get('difficulty', 2),
        'container': containers.get(mid),
        'has_container': mid in containers
    })

print(f"\nMachines: {len(machines)}")
for m in machines:
    print(f"  {m['machine_id']} - container: {m['has_container']}")

print(f"\n{'='*70}")
print("ISSUE: Your backend needs to return this:")
print(json.dumps(machines, indent=2))
