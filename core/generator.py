"""
Hackforge Main Generator
Orchestrates blueprint loading and machine generation
"""

import os
import sys
import yaml
import json
import time
from pathlib import Path
from typing import Dict, List, Optional

# Import base classes
from base import VulnerabilityBlueprint, MachineConfig, BlueprintLoader

# Import mutation engines
from mutations.broken_access_control import BrokenAccessControlMutation
from mutations.injection import InjectionMutation


class HackforgeGenerator:
    """
    Main generator class that orchestrates machine creation
    """
    
    def __init__(self, blueprints_dir: str = "blueprints"):
        self.blueprints_dir = Path(__file__).parent / blueprints_dir
        self.blueprints: Dict[str, VulnerabilityBlueprint] = {}
        self.mutation_engines = {
            'broken_access_control': BrokenAccessControlMutation,
            'injection': InjectionMutation,
        }
        
        # Load all blueprints
        self._load_blueprints()
    
    def _load_blueprints(self):
        """Load all blueprint YAML files"""
        print(f"Loading blueprints from: {self.blueprints_dir}")
        
        if not self.blueprints_dir.exists():
            print(f"⚠️ Blueprints directory not found: {self.blueprints_dir}")
            return
        
        for yaml_file in self.blueprints_dir.glob("*.yaml"):
            try:
                with open(yaml_file, 'r') as f:
                    data = yaml.safe_load(f)
                
                blueprint = BlueprintLoader.load_from_dict(data)
                
                if BlueprintLoader.validate_blueprint(blueprint):
                    self.blueprints[blueprint.blueprint_id] = blueprint
                    print(f"  ✓ Loaded: {blueprint.name} ({blueprint.blueprint_id})")
                else:
                    print(f"  ✗ Invalid blueprint: {yaml_file.name}")
                    
            except Exception as e:
                print(f"  ✗ Error loading {yaml_file.name}: {e}")
    
    def list_blueprints(self) -> List[VulnerabilityBlueprint]:
        """Get all loaded blueprints"""
        return list(self.blueprints.values())
    
    def get_blueprint(self, blueprint_id: str) -> Optional[VulnerabilityBlueprint]:
        """Get specific blueprint by ID"""
        return self.blueprints.get(blueprint_id)
    
    def generate_machine(
        self, 
        blueprint_id: str, 
        seed: str, 
        difficulty: int = 2
    ) -> Optional[MachineConfig]:
        """
        Generate a single vulnerable machine
        
        Args:
            blueprint_id: ID of the blueprint to use
            seed: Seed for deterministic generation
            difficulty: Difficulty level (1-5)
            
        Returns:
            MachineConfig object or None if failed
        """
        
        # Get blueprint
        blueprint = self.get_blueprint(blueprint_id)
        if not blueprint:
            print(f"✗ Blueprint not found: {blueprint_id}")
            return None
        
        # Validate difficulty
        min_diff, max_diff = blueprint.difficulty_range
        if not (min_diff <= difficulty <= max_diff):
            print(f"⚠️ Difficulty {difficulty} outside range {blueprint.difficulty_range}, adjusting...")
            difficulty = max(min_diff, min(difficulty, max_diff))
        
        # Get mutation engine
        engine_class = self.mutation_engines.get(blueprint.category)
        if not engine_class:
            print(f"✗ No mutation engine for category: {blueprint.category}")
            return None
        
        # Generate machine
        try:
            engine = engine_class(seed)
            config = engine.mutate(blueprint, difficulty)
            return config
        except Exception as e:
            print(f"✗ Error generating machine: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate_campaign(
        self, 
        user_id: str, 
        difficulty: int = 2,
        count: int = None
    ) -> List[MachineConfig]:
        """
        Generate a campaign of multiple machines
        
        Args:
            user_id: User identifier for seed generation
            difficulty: Difficulty level for all machines
            count: Number of machines (default: one per blueprint)
            
        Returns:
            List of MachineConfig objects
        """
        
        blueprints = list(self.blueprints.values())
        if count:
            blueprints = blueprints[:count]
        
        machines = []
        timestamp = int(time.time())
        
        print(f"\nGenerating campaign for user: {user_id}")
        print(f"Difficulty: {difficulty}")
        print(f"Machines: {len(blueprints)}")
        print("=" * 60)
        
        for i, blueprint in enumerate(blueprints, 1):
            seed = f"{user_id}_{blueprint.blueprint_id}_{timestamp}_{i}"
            
            print(f"\n[{i}/{len(blueprints)}] Generating: {blueprint.name}")
            
            machine = self.generate_machine(blueprint.blueprint_id, seed, difficulty)
            
            if machine:
                machines.append(machine)
                print(f"  ✓ Machine ID: {machine.machine_id}")
                print(f"  ✓ Variant: {machine.variant}")
                print(f"  ✓ Flag: {machine.flag['content'][:30]}...")
            else:
                print(f"  ✗ Failed to generate machine")
        
        print("\n" + "=" * 60)
        print(f"✓ Campaign generated: {len(machines)} machines")
        
        return machines
    
    def export_machine(self, machine: MachineConfig, output_dir: str = "output") -> Dict[str, str]:
        """
        Export machine configuration to files
        
        Args:
            machine: MachineConfig to export
            output_dir: Directory to save files
            
        Returns:
            Dictionary with file paths
        """
        
        output_path = Path(output_dir) / machine.machine_id
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Export config as JSON
        config_file = output_path / "config.json"
        with open(config_file, 'w') as f:
            json.dump(machine.to_dict(), f, indent=2)
        
        # Export flag
        flag_file = output_path / "flag.txt"
        with open(flag_file, 'w') as f:
            f.write(machine.flag['content'])
        
        # Export hints
        hints_file = output_path / "hints.txt"
        with open(hints_file, 'w') as f:
            f.write(f"Machine: {machine.machine_id}\n")
            f.write(f"Variant: {machine.variant}\n")
            f.write(f"Difficulty: {machine.difficulty}\n\n")
            f.write("Exploitation Hints:\n")
            for hint in machine.metadata.get('exploit_hints', []):
                f.write(f"  • {hint}\n")
        
        return {
            'config': str(config_file),
            'flag': str(flag_file),
            'hints': str(hints_file),
        }
    
    def export_campaign(self, machines: List[MachineConfig], output_dir: str = "campaigns") -> str:
        """
        Export entire campaign to directory
        
        Args:
            machines: List of MachineConfig objects
            output_dir: Base directory for campaigns
            
        Returns:
            Path to campaign directory
        """
        
        if not machines:
            return None
        
        # Use first machine's seed as campaign ID
        campaign_id = f"campaign_{int(time.time())}"
        campaign_path = Path(output_dir) / campaign_id
        campaign_path.mkdir(parents=True, exist_ok=True)
        
        # Export each machine
        for machine in machines:
            machine_dir = campaign_path / machine.machine_id
            self.export_machine(machine, str(machine_dir))
        
        # Export campaign manifest
        manifest = {
            'campaign_id': campaign_id,
            'created_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'machines': [m.to_dict() for m in machines],
            'total_machines': len(machines),
        }
        
        manifest_file = campaign_path / "campaign.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        # Export README
        readme = self._generate_campaign_readme(machines, campaign_id)
        readme_file = campaign_path / "README.md"
        with open(readme_file, 'w') as f:
            f.write(readme)
        
        return str(campaign_path)
    
    def _generate_campaign_readme(self, machines: List[MachineConfig], campaign_id: str) -> str:
        """Generate campaign README"""
        
        readme = f"""# Hackforge Campaign: {campaign_id}

Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}
Total Machines: {len(machines)}

## Machines Overview

"""
        
        for i, machine in enumerate(machines, 1):
            readme += f"""### Machine {i}: {machine.variant}
- **Machine ID**: `{machine.machine_id}`
- **Category**: {machine.blueprint_id}
- **Difficulty**: {machine.difficulty}/5
- **Flag**: `{machine.flag['content']}`

**Exploitation Hints**:
"""
            for hint in machine.metadata.get('exploit_hints', []):
                readme += f"- {hint}\n"
            
            readme += "\n---\n\n"
        
        readme += """
## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
"""
        
        return readme


def main():
    """Demo usage of the generator"""
    
    print("=" * 60)
    print("HACKFORGE - Core System Demo")
    print("Component 1: Blueprints + Mutations")
    print("=" * 60)
    print()
    
    # Initialize generator
    generator = HackforgeGenerator()
    
    print("\n" + "=" * 60)
    print("Available Blueprints:")
    print("=" * 60)
    
    for blueprint in generator.list_blueprints():
        print(f"\n{blueprint.name}")
        print(f"  ID: {blueprint.blueprint_id}")
        print(f"  Category: {blueprint.category}")
        print(f"  Variants: {len(blueprint.variants)}")
        print(f"  Difficulty Range: {blueprint.difficulty_range}")
    
    # Generate test campaign
    print("\n" + "=" * 60)
    print("Generating Test Campaign")
    print("=" * 60)
    
    machines = generator.generate_campaign(
        user_id="demo_user",
        difficulty=2,
        count=2  # Generate 2 machines (one per blueprint)
    )
    
    # Export campaign
    if machines:
        campaign_path = generator.export_campaign(machines)
        print(f"\n✓ Campaign exported to: {campaign_path}")
        print("\nYou can now inspect the generated configs and use them")
        print("in Component 2 (Template Engine) to generate actual vulnerable apps!")


if __name__ == "__main__":
    main()
