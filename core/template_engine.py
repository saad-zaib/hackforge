"""
Template Engine
Converts machine configs to deployable applications
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base import MachineConfig
from templates.base_template import TemplateRenderer


class TemplateEngine:
    """
    Main template engine that converts configs to code
    """
    
    def __init__(self, output_dir: str = "generated_machines"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_machine_app(self, config: MachineConfig) -> Dict[str, str]:
        """
        Generate complete application from machine config
        
        Args:
            config: MachineConfig object
            
        Returns:
            Dict with paths to generated files
        """
        
        print(f"\n🔨 Generating application for machine: {config.machine_id}")
        print(f"   Variant: {config.variant}")
        print(f"   Difficulty: {config.difficulty}/5")
        
        # Create machine directory
        machine_dir = self.output_dir / config.machine_id
        machine_dir.mkdir(parents=True, exist_ok=True)
        
        # Create app directory
        app_dir = machine_dir / "app"
        app_dir.mkdir(exist_ok=True)
        
        try:
            # Render templates
            rendered = TemplateRenderer.render(config)
            
            # Write application code
            app_file = app_dir / "index.php"
            app_file.write_text(rendered['code'])
            print(f"   ✓ Generated: {app_file}")
            
            # Write Dockerfile
            dockerfile = machine_dir / "Dockerfile"
            dockerfile.write_text(rendered['dockerfile'])
            print(f"   ✓ Generated: {dockerfile}")
            
            # Write flag
            flag_file = machine_dir / "flag.txt"
            flag_file.write_text(rendered['flag'])
            print(f"   ✓ Generated: {flag_file}")
            
            # Write hints
            hints_file = machine_dir / "HINTS.md"
            hints_content = f"""# Exploitation Hints

**Machine ID:** `{config.machine_id}`
**Variant:** {config.variant}
**Difficulty:** {config.difficulty}/5

## Hints

"""
            for i, hint in enumerate(rendered['hints'], 1):
                hints_content += f"{i}. {hint}\n"
            
            hints_content += f"\n## Flag\n\n`{rendered['flag']}`\n"
            hints_file.write_text(hints_content)
            print(f"   ✓ Generated: {hints_file}")
            
            # Write config
            config_file = machine_dir / "config.json"
            config_file.write_text(json.dumps(config.to_dict(), indent=2))
            print(f"   ✓ Generated: {config_file}")
            
            return {
                'machine_dir': str(machine_dir),
                'app_file': str(app_file),
                'dockerfile': str(dockerfile),
                'flag_file': str(flag_file),
                'hints_file': str(hints_file),
                'config_file': str(config_file),
            }
            
        except Exception as e:
            print(f"   ✗ Error generating machine: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _find_config_files(self, campaign_path: Path) -> List[Path]:
        """Recursively find all config.json files"""
        config_files = []
        
        for item in campaign_path.rglob("config.json"):
            # Skip if in __pycache__ or generated_machines
            if '__pycache__' not in str(item) and 'generated_machines' not in str(item):
                config_files.append(item)
        
        return config_files
    
    def generate_template(self, blueprint, language='php'):
        """Generate vulnerable code template"""

        if language.lower() == 'php':
            return self.generate_php_template(blueprint)
        elif language.lower() in ['javascript', 'js', 'node']:
            return self.generate_js_template(blueprint)
        # Add other languages

    def generate_php_template(self, blueprint):
        """Generate PHP template"""
        vuln_type = blueprint.get('vulnerability_type', 'SQL Injection')

        template = f'''<?php
// Hackforge Machine: {blueprint.get('machine_id', 'unknown')}
// Vulnerability: {vuln_type}
// Run with: php -S localhost:8000

session_start();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {{
    $username = $_POST['username'];
    $password = $_POST['password'];

    // Vulnerable query - no sanitization
    $conn = new mysqli("localhost", "root", "", "hackforge");
    $query = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
    $result = $conn->query($query);

    if ($result->num_rows > 0) {{
        echo "Login successful!";
    }} else {{
        echo "Login failed!";
    }}
}}
?>
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
    <form method="POST">
        <input type="text" name="username" placeholder="Username">
        <input type="password" name="password" placeholder="Password">
        <button type="submit">Login</button>
    </form>
</body>
</html>
'''
        return template


    def generate_campaign_apps(
        self, 
        campaign_dir: str, 
        start_port: int = 8080
    ) -> List[Dict]:
        """
        Generate applications for entire campaign
        
        Args:
            campaign_dir: Directory containing campaign configs
            start_port: Starting port number
            
        Returns:
            List of generated machine info
        """
        
        campaign_path = Path(campaign_dir)
        
        if not campaign_path.exists():
            print(f"✗ Campaign directory not found: {campaign_dir}")
            return []
        
        print(f"\n{'='*60}")
        print(f"Generating Applications for Campaign")
        print(f"{'='*60}")
        
        machines_generated = []
        port = start_port
        
        # Find all config.json files recursively
        config_files = self._find_config_files(campaign_path)
        
        print(f"\nFound {len(config_files)} machine configs")
        
        for config_file in config_files:
            print(f"\nProcessing: {config_file}")
            
            try:
                # Load config
                with open(config_file, 'r') as f:
                    config_dict = json.load(f)
                
                # Convert dict to MachineConfig
                config = MachineConfig(**config_dict)
                
                # Generate application
                result = self.generate_machine_app(config)
                
                if result:
                    result['port'] = port
                    machines_generated.append(result)
                    port += 1
                    
            except Exception as e:
                print(f"   ✗ Error processing {config_file}: {e}")
                import traceback
                traceback.print_exc()
        
        # Generate master docker-compose
        if machines_generated:
            self._generate_master_compose(machines_generated)
        
        print(f"\n{'='*60}")
        print(f"✓ Generated {len(machines_generated)} applications")
        print(f"{'='*60}\n")
        
        return machines_generated
    
    def _generate_master_compose(self, machines: List[Dict]):
        """Generate master docker-compose.yml"""
        
        compose_content = "version: '3.8'\n\nservices:\n"
        
        for i, machine in enumerate(machines, 1):
            machine_dir = Path(machine['machine_dir'])
            machine_id = machine_dir.name
            port = machine['port']
            
            # Read config to get flag location
            config_file = machine_dir / "config.json"
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            flag_location = config['flag'].get('location', '/var/www/html/flag.txt')
            
            compose_content += f"""
  machine_{i}:
    build: ./{machine_dir.relative_to(self.output_dir)}
    container_name: hackforge_machine_{i}
    ports:
      - "{port}:80"
    volumes:
      - ./{machine_dir.relative_to(self.output_dir)}/app:/var/www/html
      - ./{machine_dir.relative_to(self.output_dir)}/flag.txt:{flag_location}:ro
    environment:
      - MACHINE_ID={machine_id}
"""
        
        # Write compose file
        compose_file = self.output_dir / "docker-compose.yml"
        compose_file.write_text(compose_content)
        print(f"\n✓ Generated: {compose_file}")
        
        # Generate README
        readme_content = f"""# Hackforge Generated Machines

Generated: {len(machines)} machines

## Quick Start

```bash
# Build and start all machines
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop all machines
docker-compose down
```

## Machines

"""
        
        for i, machine in enumerate(machines, 1):
            machine_dir = Path(machine['machine_dir'])
            config_file = machine_dir / "config.json"
            
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            readme_content += f"""### Machine {i} - http://localhost:{machine['port']}

- **Variant:** {config['variant']}
- **Difficulty:** {config['difficulty']}/5
- **Machine ID:** `{config['machine_id']}`
- **Flag:** `{config['flag']['content']}`

**Hints:** See `{machine_dir.name}/HINTS.md`

---

"""
        
        readme_file = self.output_dir / "README.md"
        readme_file.write_text(readme_content)
        print(f"✓ Generated: {readme_file}")


def main():
    """Demo usage of template engine"""
    
    print("="*60)
    print("HACKFORGE - Template Engine Demo")
    print("Component 2: Code Generation")
    print("="*60)
    
    # Check if campaign exists
    campaign_dir = Path("campaigns")
    
    if not campaign_dir.exists():
        print("\n✗ No campaigns found. Run Component 1 first!")
        print("   python3 generator.py")
        return
    
    # Find latest campaign
    campaigns = sorted(campaign_dir.glob("campaign_*"))
    
    if not campaigns:
        print("\n✗ No campaigns found!")
        return
    
    latest_campaign = campaigns[-1]
    print(f"\nUsing campaign: {latest_campaign.name}")
    
    # Initialize template engine
    engine = TemplateEngine(output_dir="generated_machines")
    
    # Generate applications
    machines = engine.generate_campaign_apps(str(latest_campaign))
    
    if machines:
        print("\n" + "="*60)
        print("✓ SUCCESS! Applications generated")
        print("="*60)
        print("\nNext steps:")
        print("  1. cd generated_machines")
        print("  2. docker-compose up -d --build")
        print("  3. Access machines:")
        for i, machine in enumerate(machines, 1):
            print(f"     - Machine {i}: http://localhost:{machine['port']}")
        print("\n🎯 Try to exploit each machine and capture the flag!")
    else:
        print("\n✗ No machines generated")


if __name__ == "__main__":
    main()
