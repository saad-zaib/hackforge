#!/usr/bin/env python3
"""
Template Engine - FIXED
Ensures docker-compose properly includes database services
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base import MachineConfig

try:
    from ai_code_generator import AICodeGenerator
    from ai_docker_generator import AIDockerGenerator
    AI_AVAILABLE = True
except ImportError:
    print("⚠️ AI generators not available")
    AI_AVAILABLE = False


class AIEnhancedTemplate:
    """Template that uses AI with full blueprint config"""

    def __init__(self, config: MachineConfig, use_ai: bool = True):
        self.config = config
        self.machine_id = config.machine_id
        self.difficulty = config.difficulty
        self.variant = config.variant
        self.category = config.blueprint_id.split('_')[0]
        self.use_ai = use_ai and AI_AVAILABLE

        # Get full blueprint config from MachineConfig
        self.blueprint_config = config.blueprint_config

        if self.use_ai:
            self.ai_code_gen = AICodeGenerator()
            self.ai_docker_gen = AIDockerGenerator()
        else:
            self.ai_code_gen = None
            self.ai_docker_gen = None

    def generate_code(self) -> str:
        """Generate vulnerable application code using AI"""

        if not self.use_ai or not self.ai_code_gen or not self.blueprint_config:
            return self._fallback_code()

        print(f"  🤖 Generating with AI...")

        # Get variant config from blueprint
        variants = self.blueprint_config.get('variants', [])
        variant_config = None
        for v in variants:
            if isinstance(v, dict) and v['name'] == self.variant:
                variant_config = v
                break

        if not variant_config:
            variant_config = {'name': self.variant, 'description': '', 'exploit_example': ''}

        # Get context from mutation axes
        contexts = self.blueprint_config.get('mutation_axes', {}).get('contexts', [])
        context_name = self.config.application.get('context', 'default')

        context_config = {'name': context_name}
        for ctx in contexts:
            if isinstance(ctx, dict) and ctx.get('name') == context_name:
                context_config = ctx
                break

        # Get filters
        filters = self.config.constraints.get('filters', [])

        # Generate vulnerable code with FULL CONFIG
        vuln_function = self.ai_code_gen.generate_vulnerable_function(
            blueprint_config=self.blueprint_config,
            variant=variant_config,
            difficulty=self.difficulty,
            context=context_config,
            filters=filters
        )

        if not vuln_function:
            print("  ⚠️  AI failed, using fallback")
            return self._fallback_code()

        print(f"  ✓ Generated {len(vuln_function)} chars of PHP code")

        return self._wrap_html(vuln_function, context_config)

    def _wrap_html(self, vuln_code: str, context: Dict) -> str:
        """FIXED: Wrap AI code with proper single database connection"""

        vuln_code = vuln_code.strip()
        if vuln_code.startswith('<?php'):
            vuln_code = vuln_code[5:].strip()
        if vuln_code.endswith('?>'):
            vuln_code = vuln_code[:-2].strip()

        # Remove any database connections from AI code
        lines = vuln_code.split('\n')
        cleaned_lines = []
        skip_next = False
        
        for line in lines:
            # Skip lines that create database connections
            if 'mysqli_connect' in line or '$conn' in line or '$connection' in line:
                if 'mysqli_connect' in line:
                    skip_next = True
                continue
            if skip_next and ('die(' in line or 'Connection failed' in line):
                skip_next = False
                continue
            cleaned_lines.append(line)
        
        vuln_code = '\n'.join(cleaned_lines).strip()

        context_name = context.get('name', 'default')
        context_desc = context.get('description', 'Vulnerability challenge')

        # Check if we need database
        needs_db = False
        if self.blueprint_config:
            infrastructure = self.blueprint_config.get('infrastructure', {})
            needs_db = infrastructure.get('needs_database', False)

        # Build PHP header with SINGLE DB connection if needed
        php_header = f'''<?php
/**
 * Machine: {self.machine_id}
 * Variant: {self.variant}
 * Difficulty: {self.difficulty}/5
 * Context: {context_name}
 */
'''

        if needs_db:
            db_type = self.blueprint_config.get('infrastructure', {}).get('database_type', 'mysql')
            if db_type == 'mysql':
                # FIXED: Use consistent connection variable name
                php_header += f'''
// Database connection
$conn = mysqli_connect('db_{self.machine_id}', 'hackforge', 'hackforge123', 'hackforge');
if (!$conn) {{
    die('<div class="error">Connection failed: ' . mysqli_connect_error() . '</div>');
}}
'''

        php_header += '''
// Process user input if provided
if (isset($_GET['input'])) {
'''

        php_footer = '''
}
'''

        if needs_db:
            php_footer += '''
mysqli_close($conn);
'''

        php_footer += '?>'

        # Replace any $connection with $conn in AI code
        vuln_code = vuln_code.replace('$connection', '$conn')

        return php_header + vuln_code + php_footer + f'''
<!DOCTYPE html>
<html>
<head>
    <title>{self.variant}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            max-width: 900px;
            margin: 50px auto;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #fff;
            padding: 20px;
        }}
        .container {{
            background: rgba(42, 42, 42, 0.95);
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
            border: 1px solid rgba(231, 76, 60, 0.3);
        }}
        h1 {{
            color: #e74c3c;
            margin-bottom: 10px;
            font-size: 2em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .info {{
            background: rgba(52, 73, 94, 0.5);
            padding: 15px;
            border-radius: 6px;
            margin: 20px 0;
            border-left: 4px solid #3498db;
        }}
        .info strong {{ color: #3498db; }}
        input, button {{
            padding: 14px;
            margin: 10px 0;
            font-size: 16px;
            width: 100%;
            box-sizing: border-box;
            border-radius: 6px;
        }}
        input {{
            background: #2c3e50;
            border: 2px solid #34495e;
            color: #ecf0f1;
            transition: border-color 0.3s;
        }}
        input:focus {{
            outline: none;
            border-color: #e74c3c;
        }}
        button {{
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
            color: white;
            border: none;
            cursor: pointer;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(231, 76, 60, 0.4);
        }}
        .result, .error, .output {{
            margin-top: 20px;
            padding: 20px;
            background: rgba(44, 62, 80, 0.5);
            border-left: 4px solid #e74c3c;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
        }}
        .error {{
            border-left-color: #e67e22;
            background: rgba(230, 126, 34, 0.1);
        }}
        .output {{
            border-left-color: #27ae60;
            background: rgba(39, 174, 96, 0.1);
        }}
        pre {{
            white-space: pre-wrap;
            word-wrap: break-word;
            margin: 0;
            color: #ecf0f1;
        }}
        .hint {{
            margin-top: 20px;
            padding: 20px;
            background: rgba(26, 71, 42, 0.5);
            border-left: 4px solid #27ae60;
            border-radius: 6px;
            font-size: 14px;
        }}
        .hint strong {{ color: #2ecc71; }}
        code {{
            background: rgba(52, 152, 219, 0.2);
            padding: 2px 6px;
            border-radius: 3px;
            color: #3498db;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 {self.variant}</h1>

        <div class="info">
            <p><strong>Context:</strong> {context_desc}</p>
            <p><strong>Difficulty:</strong> {self.difficulty}/5</p>
            <p><strong>Machine ID:</strong> <code>{self.machine_id}</code></p>
        </div>

        <form method="GET">
            <input
                name="input"
                placeholder="Enter your payload here..."
                value="<?php echo isset($_GET['input']) ? htmlspecialchars($_GET['input']) : ''; ?>"
                autofocus
            >
            <button type="submit">🚀 Execute</button>
        </form>

        <div class="hint">
            <strong>💡 Challenge Hint:</strong> Try to exploit the {self.variant.lower()} in the {context_name} context.
        </div>
    </div>
</body>
</html>'''

    def _fallback_code(self) -> str:
        """Fallback template"""
        return f'''<?php
if (isset($_GET['input'])) {{
    $input = $_GET['input'];
    echo '<div class="output"><pre>' . htmlspecialchars($input) . '</pre></div>';
}}
?>
<!DOCTYPE html>
<html>
<head><title>{self.variant}</title></head>
<body>
    <h1>{self.variant}</h1>
    <form method="GET">
        <input name="input" placeholder="Enter input">
        <button>Submit</button>
    </form>
</body>
</html>'''

    def generate_dockerfile(self) -> str:
        """Generate Dockerfile using blueprint config"""

        if self.use_ai and self.ai_docker_gen and self.blueprint_config:
            return self.ai_docker_gen.generate_dockerfile_from_config(self.blueprint_config)

        return self._fallback_dockerfile()

    def _fallback_dockerfile(self) -> str:
        """Fallback Dockerfile"""

        if not self.blueprint_config:
            return self._basic_dockerfile()

        infrastructure = self.blueprint_config.get('infrastructure', {})
        docker_reqs = infrastructure.get('docker_requirements', {})

        base_image = docker_reqs.get('base_image', 'php:8.0-apache')
        extensions = docker_reqs.get('extensions', [])
        packages = docker_reqs.get('packages', [])

        dockerfile = f'''FROM {base_image}

RUN apt-get update && apt-get install -y \\
    iputils-ping whois dnsutils net-tools curl wget \\
'''

        if packages:
            for pkg in packages:
                dockerfile += f'    {pkg} \\\n'

        dockerfile += '    && rm -rf /var/lib/apt/lists/*\n\n'

        if extensions:
            ext_list = ' '.join(extensions)
            dockerfile += f'RUN docker-php-ext-install {ext_list}\n\n'

        dockerfile += '''RUN a2enmod rewrite

EXPOSE 80

CMD ["apache2-foreground"]
'''
        return dockerfile

    def _basic_dockerfile(self) -> str:
        """Most basic Dockerfile"""
        return '''FROM php:8.0-apache

RUN apt-get update && apt-get install -y \\
    iputils-ping whois dnsutils net-tools curl wget \\
    && rm -rf /var/lib/apt/lists/*

RUN a2enmod rewrite

EXPOSE 80

CMD ["apache2-foreground"]
'''

    def generate_setup_files(self) -> dict:
        """Generate setup files using blueprint config"""

        files = {}

        if not self.blueprint_config:
            return files

        infrastructure = self.blueprint_config.get('infrastructure', {})

        # Database setup
        if infrastructure.get('needs_database') and self.use_ai and self.ai_code_gen:
            schema, _ = self.ai_code_gen.generate_database_setup(
                blueprint_config=self.blueprint_config,
                flag=self.config.flag['content']
            )

            if schema:
                db_type = infrastructure.get('database_type', 'mysql')
                if db_type == 'mysql':
                    files['init.sql'] = schema
                elif db_type == 'mongodb':
                    files['init.js'] = schema

        # File structure
        if infrastructure.get('needs_file_system') and self.use_ai and self.ai_code_gen:
            file_structure = self.ai_code_gen.generate_file_structure(
                blueprint_config=self.blueprint_config,
                flag=self.config.flag['content']
            )

            if file_structure:
                files['setup.sh'] = self._generate_file_setup_script(file_structure)

        return files

    def _generate_file_setup_script(self, file_structure: Dict[str, str]) -> str:
        """Generate bash script to create file structure"""

        script = "#!/bin/bash\n\n"
        script += "# Setup file structure for vulnerability\n\n"

        for filepath, content in file_structure.items():
            # Escape content for bash
            content_escaped = content.replace('"', '\\"').replace('$', '\\$')

            # Create directory if needed
            dir_path = os.path.dirname(filepath)
            if dir_path:
                script += f'mkdir -p {dir_path}\n'

            script += f'echo "{content_escaped}" > {filepath}\n'
            script += f'chmod 644 {filepath}\n\n'

        return script


class TemplateEngine:
    """Template engine with AI code and Docker generation"""

    def __init__(self, machines_dir: str = "generated_machines", use_ai: bool = True):
        self.machines_dir = Path(machines_dir)
        self.use_ai = use_ai and AI_AVAILABLE

        if not self.machines_dir.exists():
            self.machines_dir.mkdir(parents=True, exist_ok=True)

        if self.use_ai:
            print("🤖 AI Generation: ENABLED (Code + Docker)")
            self.ai_docker_gen = AIDockerGenerator()
        else:
            print("📝 Using static templates")
            self.ai_docker_gen = None

    def generate_machine_app(self, config: MachineConfig, machine_dir: Path) -> dict:
        """Generate complete application with Docker setup"""

        print(f"\n🔨 Generating: {config.machine_id}")
        print(f"   Variant: {config.variant}")
        print(f"   Category: {config.blueprint_id.split('_')[0]}")

        if config.blueprint_config:
            print(f"   ✓ Blueprint config loaded ({len(json.dumps(config.blueprint_config))} bytes)")
        else:
            print(f"   ⚠️  No blueprint config - using fallback")

        app_dir = machine_dir / "app"
        app_dir.mkdir(exist_ok=True)

        category = config.blueprint_id.split('_')[0]

        try:
            # 1. Generate vulnerable code
            template = AIEnhancedTemplate(config, use_ai=self.use_ai)

            app_code = template.generate_code()
            if not app_code:
                print("   ✗ Code generation failed")
                return None

            app_file = app_dir / "index.php"
            app_file.write_text(app_code)
            print(f"   ✓ Code: {app_file}")

            # 2. Generate Dockerfile
            dockerfile = template.generate_dockerfile()
            dockerfile_path = machine_dir / "Dockerfile"
            dockerfile_path.write_text(dockerfile)
            print(f"   ✓ Dockerfile: {dockerfile_path}")

            # 3. Generate setup files (DB schema, file structure)
            setup_files = template.generate_setup_files()

            for filename, content in setup_files.items():
                filepath = machine_dir / filename
                filepath.write_text(content)
                print(f"   ✓ Setup: {filepath}")

            # 4. Write flag and hints
            flag_file = machine_dir / "flag.txt"
            flag_file.write_text(config.flag['content'])

            hints_file = machine_dir / "HINTS.md"
            hints_file.write_text(self._generate_hints(config))

            return {
                'machine_id': config.machine_id,
                'machine_dir': str(machine_dir),
                'category': category,
                'port': None,  # Will be set later
                'ai_generated': self.use_ai and bool(config.blueprint_config)
            }

        except Exception as e:
            print(f"   ✗ Error: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _generate_hints(self, config: MachineConfig) -> str:
        """Generate hints markdown"""
        hints = config.metadata.get('exploit_hints', [])

        content = f"""# {config.variant}

**Machine ID:** `{config.machine_id}`
**Difficulty:** {config.difficulty}/5
**Category:** {config.blueprint_id}

## Hints

"""
        for i, hint in enumerate(hints, 1):
            content += f"{i}. {hint}\n"

        content += f"\n## Flag\n\n`{config.flag['content']}`\n"
        return content

    def process_all_machines(self, start_port: int = 8080) -> list:
        """FIXED: Process all machines and ALWAYS generate proper docker-compose"""

        print(f"\n{'='*60}")
        print(f"Processing Machines: {self.machines_dir}")
        print(f"{'='*60}")

        machines_generated = []
        port = start_port

        machine_dirs = [
            d for d in self.machines_dir.iterdir()
            if d.is_dir() and not d.name.startswith('.') and (d / "config.json").exists()
        ]

        print(f"\nFound {len(machine_dirs)} machine(s)\n")

        # Collect blueprint configs
        blueprint_configs = {}

        for machine_dir in machine_dirs:
            config_file = machine_dir / "config.json"

            try:
                with open(config_file, 'r') as f:
                    config_dict = json.load(f)

                config = MachineConfig(**config_dict)
                result = self.generate_machine_app(config, machine_dir)

                if result:
                    result['port'] = port
                    machines_generated.append(result)
                    
                    # Store blueprint config
                    if config.blueprint_config:
                        category = config.blueprint_id.split('_')[0]
                        blueprint_configs[category] = config.blueprint_config
                    
                    port += 1

            except Exception as e:
                print(f"   ✗ Error: {e}")

        # ALWAYS generate docker-compose
        if machines_generated:
            self._generate_compose(machines_generated, blueprint_configs)

        print(f"\n{'='*60}")
        print(f"✓ Generated {len(machines_generated)} application(s)")
        print(f"{'='*60}\n")

        return machines_generated

    def _generate_compose(self, machines: list, blueprint_configs: Dict[str, Dict]):
        """FIXED: Always generate proper docker-compose with databases"""

        print(f"\n{'='*60}")
        print(f"DOCKER-COMPOSE GENERATION")
        print(f"{'='*60}")

        # Use AI docker generator with collected configs
        if self.use_ai and self.ai_docker_gen and blueprint_configs:
            print(f"🤖 Generating with AI ({len(blueprint_configs)} configs)...")
            compose_content = self.ai_docker_gen.generate_docker_compose(machines, blueprint_configs)
        else:
            print(f"📝 Generating basic compose...")
            compose_content = self._generate_basic_compose(machines)

        compose_file = self.machines_dir / "docker-compose.yml"
        compose_file.write_text(compose_content)
        print(f"✓ Generated: {compose_file}")

    def _generate_basic_compose(self, machines: list) -> str:
        """Fallback: Basic docker-compose"""
        compose = "version: '3.8'\n\nservices:\n"

        for machine in machines:
            machine_id = machine['machine_id']
            port = machine['port']

            compose += f"""
  {machine_id}:
    build: ./{machine_id}
    container_name: hackforge_{machine_id}
    ports:
      - "{port}:80"
    volumes:
      - ./{machine_id}/app:/var/www/html
    restart: unless-stopped
"""

        return compose


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Hackforge Template Engine with AI')
    parser.add_argument('--machines-dir', default='generated_machines')
    parser.add_argument('--port', type=int, default=8080)
    parser.add_argument('--no-ai', action='store_true')
    args = parser.parse_args()

    print("="*60)
    print("HACKFORGE - AI Template & Docker Engine - FIXED")
    print("="*60)

    engine = TemplateEngine(
        machines_dir=args.machines_dir,
        use_ai=not args.no_ai
    )

    machines = engine.process_all_machines(start_port=args.port)

    if machines:
        print("\nNext steps:")
        print(f"  cd {args.machines_dir}")
        print(f"  docker-compose up -d --build")
        print(f"\nMachines:")
        for m in machines:
            ai_emoji = '🤖' if m.get('ai_generated') else '📝'
            print(f"  {ai_emoji} http://localhost:{m['port']} - {m['machine_id']}")


if __name__ == "__main__":
    main()
