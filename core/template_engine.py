#!/usr/bin/env python3
"""
Template Engine - INDIVIDUAL DOCKER-COMPOSE PER MACHINE
Each machine gets its own docker-compose.yml for independent management
"""

import os
import sys
import json
import re
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

    def _clean_ai_php_code(self, code: str) -> str:
        """Safely clean AI-generated PHP code without breaking syntax"""
        code = code.strip()
        if code.startswith('<?php'):
            code = code[5:].strip()
        if code.endswith('?>'):
            code = code[:-2].strip()

        # Replace any database connection variables with our standard $conn
        code = re.sub(r'\$connection\s*=', '$conn =', code)
        code = re.sub(r'\$db\s*=', '$conn =', code)
        code = re.sub(r'\$link\s*=', '$conn =', code)
        
        # Replace all references to old variable names
        code = re.sub(r'\$connection\b', '$conn', code)
        code = re.sub(r'\$db\b(?!\w)', '$conn', code)
        code = re.sub(r'\$link\b', '$conn', code)

        # Remove duplicate mysqli_connect calls
        lines = code.split('\n')
        cleaned_lines = []
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith('$conn') and 'mysqli_connect' in stripped and stripped.endswith(';'):
                continue
            
            if 'mysqli_connect_error' in stripped:
                continue
                
            cleaned_lines.append(line)

        return '\n'.join(cleaned_lines).strip()

    def _wrap_html(self, vuln_code: str, context: Dict) -> str:
        """Wrap AI code with proper single database connection"""

        vuln_code = self._clean_ai_php_code(vuln_code)

        context_name = context.get('name', 'default')
        context_desc = context.get('description', 'Vulnerability challenge')

        # Check if we need database
        needs_db = False
        db_host = 'localhost'  # Default for individual compose
        
        if self.blueprint_config:
            infrastructure = self.blueprint_config.get('infrastructure', {})
            needs_db = infrastructure.get('needs_database', False)
            
            # For individual docker-compose, database is in same compose file
            if needs_db:
                db_type = infrastructure.get('database_type', 'mysql')
                if db_type == 'mysql':
                    db_host = 'db'  # Service name in docker-compose
                elif db_type == 'mongodb':
                    db_host = 'mongodb'

        # Build PHP header
        php_header = f'''<?php
/**
 * Machine: {self.machine_id}
 * Variant: {self.variant}
 * Difficulty: {self.difficulty}/5
 * Context: {context_name}
 */
'''

        if needs_db:
            php_header += f'''
// Database connection
$conn = mysqli_connect('{db_host}', 'hackforge', 'hackforge123', 'hackforge');
if (!$conn) {{
    die('<div class="error">Connection failed: ' . mysqli_connect_error() . '</div>');
}}

'''

        php_header += '''// Process user input if provided
if (isset($_GET['input'])) {
    $input = $_GET['input'];
    
'''

        # Indent the vulnerable code
        indented_code = '\n'.join('    ' + line if line.strip() else '' for line in vuln_code.split('\n'))

        php_footer = '''\n}
'''

        if needs_db:
            php_footer += '''
// Close database connection
mysqli_close($conn);
'''

        php_footer += '?>'

        # Combine everything
        full_php = php_header + indented_code + php_footer

        # Validate PHP syntax
        if not self._validate_php_syntax(full_php):
            print("  ⚠️ PHP syntax validation failed, using fallback")
            return self._fallback_code()

        return full_php + f'''
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

    def _validate_php_syntax(self, php_code: str) -> bool:
        """Validate PHP syntax by counting braces"""
        code_without_strings = re.sub(r'"[^"]*"', '""', php_code)
        code_without_strings = re.sub(r"'[^']*'", "''", code_without_strings)
        
        open_braces = code_without_strings.count('{')
        close_braces = code_without_strings.count('}')
        
        if open_braces != close_braces:
            print(f"  ⚠️ Brace mismatch: {open_braces} open, {close_braces} close")
            return False
        
        open_parens = code_without_strings.count('(')
        close_parens = code_without_strings.count(')')
        
        if open_parens != close_parens:
            print(f"  ⚠️ Parenthesis mismatch: {open_parens} open, {close_parens} close")
            return False
            
        return True

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

        return files

    def generate_individual_compose(self, port: int) -> str:
        """
        NEW: Generate individual docker-compose.yml for this machine
        This allows independent management of each machine
        """
        
        needs_db = False
        db_type = None
        
        if self.blueprint_config:
            infrastructure = self.blueprint_config.get('infrastructure', {})
            needs_db = infrastructure.get('needs_database', False)
            db_type = infrastructure.get('database_type', 'mysql')

        compose = f'''version: '3.8'

services:
  web:
    build: .
    container_name: hackforge_{self.machine_id}
    ports:
      - "{port}:80"
    volumes:
      - ./app:/var/www/html
'''

        if needs_db:
            compose += f'''    depends_on:
      - db
    networks:
      - hackforge_{self.machine_id}
'''
        else:
            compose += f'''    networks:
      - hackforge_{self.machine_id}
'''

        compose += '''    restart: unless-stopped

'''

        # Add database service if needed
        if needs_db:
            if db_type == 'mysql':
                compose += f'''  db:
    image: mysql:8.0
    container_name: hackforge_db_{self.machine_id}
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: hackforge
      MYSQL_USER: hackforge
      MYSQL_PASSWORD: hackforge123
    volumes:
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
      - db_data:/var/lib/mysql
    networks:
      - hackforge_{self.machine_id}
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

'''
            elif db_type == 'mongodb':
                compose += f'''  mongodb:
    image: mongo:5.0
    container_name: hackforge_mongodb_{self.machine_id}
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: root123
    volumes:
      - ./init.js:/docker-entrypoint-initdb.d/init.js
      - mongo_data:/data/db
    networks:
      - hackforge_{self.machine_id}
    restart: unless-stopped

'''

        # Add networks section
        compose += f'''networks:
  hackforge_{self.machine_id}:
    driver: bridge

'''

        # Add volumes section if database exists
        if needs_db:
            compose += '''volumes:
'''
            if db_type == 'mysql':
                compose += '''  db_data:
'''
            elif db_type == 'mongodb':
                compose += '''  mongo_data:
'''

        return compose


class TemplateEngine:
    """Template engine that generates INDIVIDUAL docker-compose per machine"""

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

    def generate_machine_app(self, config: MachineConfig, machine_dir: Path, port: int) -> dict:
        """Generate complete application with INDIVIDUAL docker-compose"""

        print(f"\n🔨 Generating: {config.machine_id}")
        print(f"   Variant: {config.variant}")
        print(f"   Category: {config.blueprint_id.split('_')[0]}")
        print(f"   Port: {port}")

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

            # 3. Generate INDIVIDUAL docker-compose.yml
            compose_content = template.generate_individual_compose(port)
            compose_file = machine_dir / "docker-compose.yml"
            compose_file.write_text(compose_content)
            print(f"   ✓ Docker Compose: {compose_file}")

            # 4. Generate setup files (DB schema, etc.)
            setup_files = template.generate_setup_files()

            for filename, content in setup_files.items():
                filepath = machine_dir / filename
                filepath.write_text(content)
                print(f"   ✓ Setup: {filepath}")

            # 5. Write flag and hints
            flag_file = machine_dir / "flag.txt"
            flag_file.write_text(config.flag['content'])

            hints_file = machine_dir / "HINTS.md"
            hints_file.write_text(self._generate_hints(config))

            # 6. Generate start/stop scripts
            self._generate_management_scripts(machine_dir, config.machine_id, port)

            return {
                'machine_id': config.machine_id,
                'machine_dir': str(machine_dir),
                'category': category,
                'port': port,
                'ai_generated': self.use_ai and bool(config.blueprint_config)
            }

        except Exception as e:
            print(f"   ✗ Error: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _generate_management_scripts(self, machine_dir: Path, machine_id: str, port: int):
        """Generate convenience scripts for managing this machine"""
        
        # Start script
        start_script = f'''#!/bin/bash
# Start {machine_id}
echo "🚀 Starting {machine_id}..."
docker-compose up -d --build

echo "✓ Machine running at: http://localhost:{port}"
echo "✓ Container: hackforge_{machine_id}"
echo ""
echo "View logs: docker-compose logs -f"
echo "Stop: docker-compose down"
'''
        
        start_file = machine_dir / "start.sh"
        start_file.write_text(start_script)
        start_file.chmod(0o755)
        
        # Stop script
        stop_script = f'''#!/bin/bash
# Stop {machine_id}
echo "🛑 Stopping {machine_id}..."
docker-compose down
echo "✓ Machine stopped"
'''
        
        stop_file = machine_dir / "stop.sh"
        stop_file.write_text(stop_script)
        stop_file.chmod(0o755)

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
        """Process all machines with INDIVIDUAL docker-compose files"""

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

        for machine_dir in machine_dirs:
            config_file = machine_dir / "config.json"

            try:
                with open(config_file, 'r') as f:
                    config_dict = json.load(f)

                config = MachineConfig(**config_dict)
                result = self.generate_machine_app(config, machine_dir, port)

                if result:
                    machines_generated.append(result)
                    port += 1

            except Exception as e:
                print(f"   ✗ Error: {e}")

        # Generate master management script
        if machines_generated:
            self._generate_master_scripts(machines_generated)

        print(f"\n{'='*60}")
        print(f"✓ Generated {len(machines_generated)} application(s)")
        print(f"{'='*60}\n")

        return machines_generated

    def _generate_master_scripts(self, machines: list):
        """Generate master scripts to manage all machines"""
        
        # Start all script
        start_all = '''#!/bin/bash
# Start all Hackforge machines

echo "🚀 Starting all machines..."
echo ""

'''
        for m in machines:
            machine_id = m['machine_id']
            start_all += f'''echo "Starting {machine_id}..."
cd {machine_id} && docker-compose up -d --build && cd ..

'''

        start_all += '''
echo ""
echo "✓ All machines started!"
echo ""
echo "Active machines:"
'''

        for m in machines:
            start_all += f'''echo "  • http://localhost:{m['port']} - {m['machine_id']}"
'''

        start_file = self.machines_dir / "start_all.sh"
        start_file.write_text(start_all)
        start_file.chmod(0o755)
        print(f"✓ Master script: {start_file}")

        # Stop all script
        stop_all = '''#!/bin/bash
# Stop all Hackforge machines

echo "🛑 Stopping all machines..."
echo ""

'''
        for m in machines:
            machine_id = m['machine_id']
            stop_all += f'''echo "Stopping {machine_id}..."
cd {machine_id} && docker-compose down && cd ..

'''

        stop_all += '''
echo ""
echo "✓ All machines stopped!"
'''

        stop_file = self.machines_dir / "stop_all.sh"
        stop_file.write_text(stop_all)
        stop_file.chmod(0o755)
        print(f"✓ Master script: {stop_file}")

        # List machines script
        list_script = '''#!/bin/bash
# List all Hackforge machines

echo "📋 Hackforge Machines"
echo "===================="
echo ""

'''
        for m in machines:
            list_script += f'''echo "{m['machine_id']}"
echo "  Port: {m['port']}"
echo "  Category: {m['category']}"
echo "  URL: http://localhost:{m['port']}"
cd {m['machine_id']} && echo -n "  Status: " && docker-compose ps --services --filter "status=running" | wc -l | awk '{{if ($1 > 0) print "🟢 Running"; else print "⚫ Stopped"}}' && cd ..
echo ""

'''

        list_file = self.machines_dir / "list_machines.sh"
        list_file.write_text(list_script)
        list_file.chmod(0o755)
        print(f"✓ Master script: {list_file}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Hackforge Template Engine - Individual Compose')
    parser.add_argument('--machines-dir', default='generated_machines')
    parser.add_argument('--port', type=int, default=8080)
    parser.add_argument('--no-ai', action='store_true')
    args = parser.parse_args()

    print("="*60)
    print("HACKFORGE - INDIVIDUAL DOCKER-COMPOSE ENGINE")
    print("="*60)

    engine = TemplateEngine(
        machines_dir=args.machines_dir,
        use_ai=not args.no_ai
    )

    machines = engine.process_all_machines(start_port=args.port)

    if machines:
        print("\n" + "="*60)
        print("MANAGEMENT COMMANDS")
        print("="*60)
        print(f"\nIndividual machines:")
        for m in machines:
            ai_emoji = '🤖' if m.get('ai_generated') else '📝'
            print(f"  {ai_emoji} cd {m['machine_id']} && ./start.sh")
        
        print(f"\nMaster commands (from {args.machines_dir}/):")
        print(f"  Start all:  ./start_all.sh")
        print(f"  Stop all:   ./stop_all.sh")
        print(f"  List:       ./list_machines.sh")
        
        print(f"\nURLs:")
        for m in machines:
            print(f"  • http://localhost:{m['port']} - {m['machine_id']}")
        print()


if __name__ == "__main__":
    main()
