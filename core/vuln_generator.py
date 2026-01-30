#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path


class VulnerabilityGenerator:

    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.vuln_id = self.config['vulnerability_id']
        self.vuln_name = self.config['name']
        self.category = self.config['category']

    def generate_all(self, base_dir: str = "."):
        """Generate all three components in their respective directories"""

        # Create directories if they don't exist
        blueprint_dir = os.path.join(base_dir, "blueprints")
        mutation_dir = os.path.join(base_dir, "mutations")
        template_dir = os.path.join(base_dir, "templates")

        os.makedirs(blueprint_dir, exist_ok=True)
        os.makedirs(mutation_dir, exist_ok=True)
        os.makedirs(template_dir, exist_ok=True)

        # Use category for all filenames for consistency
        blueprint_path = os.path.join(blueprint_dir, f"{self.category}_blueprint.yaml")
        mutation_path = os.path.join(mutation_dir, f"{self.category}_mutation.py")
        template_path = os.path.join(template_dir, f"{self.category}_templates.py")

        with open(blueprint_path, 'w') as f:
            f.write(self.generate_blueprint())

        with open(mutation_path, 'w') as f:
            f.write(self.generate_mutation())

        with open(template_path, 'w') as f:
            f.write(self.generate_template())

        print(f"✅ Blueprint: {blueprint_path}")
        print(f"✅ Mutation:  {mutation_path}")
        print(f"✅ Template:  {template_path}")
        print(f"\n💡 All files use category '{self.category}' for consistency")

    def generate_blueprint(self) -> str:
        """Generate blueprint YAML content"""

        variants = self.config.get('variants', [])
        entry_points = self.config.get('entry_points', [])
        mutation_axes = self.config.get('mutation_axes', {})
        infrastructure = self.config.get('infrastructure', {})
        database_schema = self.config.get('database_schema', {})

        # Extract variant names for simple list
        variant_names = [v['name'] if isinstance(v, dict) else v for v in variants]
        
        # Extract entry point types for simple list
        entry_point_types = [ep['type'] if isinstance(ep, dict) else ep for ep in entry_points]

        blueprint = f"""blueprint_id: {self.vuln_id}

name: {self.vuln_name}

category: {self.category}

difficulty_range: {self.config.get('difficulty_range', [1, 5])}

description: |
  {self.config.get('description', 'Vulnerability description')}

infrastructure:
{self._format_infrastructure(infrastructure)}

database_schema:
{self._format_database_schema(database_schema)}

variants:
{self._format_list(variant_names)}

entry_points:
{self._format_list(entry_point_types)}

mutation_axes:
{self._format_mutation_axes(mutation_axes)}
"""
        return blueprint

    def generate_mutation(self) -> str:
        """Generate mutation engine Python code"""

        class_name = self._to_class_name(self.category) + "Mutation"
        variants = self.config.get('variants', [])
        variant_names = [v['name'] if isinstance(v, dict) else v for v in variants]

        # Generate variant methods
        variant_methods = []
        for variant in variants:
            variant_obj = variant if isinstance(variant, dict) else {'name': variant}
            method_name = self._to_method_name(variant_obj['name'])
            variant_methods.append(self._generate_variant_method(variant_obj, method_name))

        mutation_code = f'''"""
{self.vuln_name} Mutation Engine
Generates unique variants of {self.vuln_name.lower()} vulnerabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base import MutationEngine, VulnerabilityBlueprint, MachineConfig
from typing import Dict, List, Any


class {class_name}(MutationEngine):
    """
    Mutation engine for {self.vuln_name} vulnerabilities
    """

    def mutate(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> MachineConfig:
        """Generate unique {self.vuln_name.lower()} machine configuration"""

        # Select variant based on difficulty
        variant = self._select_variant(blueprint.variants, difficulty)

        # Generate machine ID
        machine_id = self.generate_machine_id()

        # Generate configuration based on variant
{self._generate_variant_dispatch(variant_names)}

        # Create machine config
        return MachineConfig(
            machine_id=machine_id,
            blueprint_id=blueprint.blueprint_id,
            variant=variant,
            difficulty=difficulty,
            seed=self.seed,
            application=config['application'],
            constraints=config['constraints'],
            flag=config['flag'],
            behavior=config['behavior'],
            metadata=config['metadata']
        )

    def _select_variant(self, variants: List[str], difficulty: int) -> str:
        """Select variant based on difficulty level"""
        if difficulty <= 2:
            easy_variants = variants[:len(variants)//2] if len(variants) > 2 else variants
            return self.select_random(easy_variants)
        else:
            return self.select_random(variants)

{chr(10).join(variant_methods)}

    def _get_filter_codes(self, filter_names: List[str]) -> List[Dict]:
        """Convert filter names to filter code objects"""
        filter_map = {{
{self._generate_filter_map()}
        }}

        return [filter_map[f] for f in filter_names if f in filter_map]

    def _generate_hints(self, filters: List[Dict], context: str, difficulty: int) -> List[str]:
        """Generate context-specific hints"""
        hints = [
            f"Context: {{context}}",
            f"Difficulty: {{difficulty}}/5",
        ]

        if not filters:
            hints.append("✓ No input filtering - direct attack possible")
        else:
            hints.append(f"⚠️ Filters active: {{', '.join([f['type'] for f in filters])}}")

        if difficulty <= 2:
            hints.append("💡 Try basic payloads first")

        return hints
'''
        return mutation_code

    def generate_template(self) -> str:
        """Generate template Python code WITH THEME SUPPORT"""

        class_name = self._to_class_name(self.category) + "Template"
        variants = self.config.get('variants', [])
        variant_names = [v['name'] if isinstance(v, dict) else v for v in variants]
        infrastructure = self.config.get('infrastructure', {})
        needs_db = infrastructure.get('needs_database', False)

        # Generate variant template methods
        variant_templates = []
        for variant in variants:
            variant_obj = variant if isinstance(variant, dict) else {'name': variant}
            method_name = self._to_method_name(variant_obj['name'])
            variant_templates.append(self._generate_template_method(variant_obj, method_name, needs_db))

        template_code = f'''"""
{self.vuln_name} Vulnerability Templates
Generates vulnerable applications with theme variety
"""

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from base_template import BaseTemplate
from theme_library import ThemeLibrary
from typing import Dict


class {class_name}(BaseTemplate):
    """
    Template generator for {self.vuln_name.lower()} vulnerabilities
    """

    def __init__(self, config):
        super().__init__(config)
        # Pick random theme for this machine
        self.theme_name, self.theme = ThemeLibrary.get_random_theme()
        print(f"  🎨 Theme: {{self.theme['name']}}")

    def generate_code(self) -> str:
        """Generate vulnerable application based on variant"""

        variant = self.config.variant

{self._generate_template_dispatch(variant_names)}

{chr(10).join(variant_templates)}

    def _generate_filter_code(self, filters: list, language: str) -> str:
        """Generate filter code from filter list"""
        if not filters:
            return ""

        if language == 'php':
            return "\\n            ".join([f['php_code'] for f in filters])
        elif language == 'python':
            return "\\n    ".join([f['python_code'] for f in filters])

        return ""

    def generate_dockerfile(self) -> str:
        """Generate Dockerfile for {self.vuln_name.lower()} vulnerabilities"""

{self._generate_dockerfile_method()}
'''
        return template_code

    # Helper methods

    def _format_infrastructure(self, infra: dict) -> str:
        """Format infrastructure section for YAML"""
        if not infra:
            return "  needs_database: false"
        
        lines = []
        lines.append(f"  needs_database: {str(infra.get('needs_database', False)).lower()}")
        if infra.get('database_type'):
            lines.append(f"  database_type: {infra['database_type']}")
        lines.append(f"  needs_file_system: {str(infra.get('needs_file_system', False)).lower()}")
        lines.append(f"  needs_external_service: {str(infra.get('needs_external_service', False)).lower()}")
        
        return '\n'.join(lines)

    def _format_database_schema(self, schema: dict) -> str:
        """Format database schema section for YAML"""
        if not schema:
            return "  tables: []"
        
        lines = []
        lines.append("  tables:")
        for table in schema.get('tables', []):
            lines.append(f"    - name: {table['name']}")
            lines.append("      columns:")
            for col in table['columns']:
                lines.append(f"        - {col}")
        
        if schema.get('flag_location'):
            lines.append(f"  flag_location: {schema['flag_location']}")
        
        return '\n'.join(lines)

    def _format_list(self, items: list) -> str:
        """Format list for YAML"""
        return '\n'.join([f"  - {item}" for item in items])

    def _format_mutation_axes(self, axes: dict) -> str:
        """Format mutation axes for YAML"""
        result = []
        for key, value in axes.items():
            result.append(f"  {key}:")
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    result.append(f"    {subkey}:")
                    if isinstance(subvalue, list):
                        for item in subvalue:
                            if isinstance(item, dict):
                                result.append(f"      - name: {item.get('name', 'unknown')}")
                            else:
                                result.append(f"      - {item}")
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        result.append(f"    - name: {item.get('name', 'unknown')}")
                    else:
                        result.append(f"    - {item}")
        return '\n'.join(result)

    def _to_class_name(self, name: str) -> str:
        """Convert name to class name - FIXED to handle underscores"""
        # Replace both hyphens and underscores with spaces, then capitalize each word
        words = name.replace('-', ' ').replace('_', ' ').split()
        return ''.join(word.capitalize() for word in words)

    def _to_method_name(self, name: str) -> str:
        """Convert name to method name"""
        return '_generate_' + name.lower().replace(' ', '_').replace('-', '_')

    def _generate_variant_dispatch(self, variants: list) -> str:
        """Generate if-elif chain for variant dispatch"""
        lines = []
        for i, variant in enumerate(variants):
            variant_name = variant if isinstance(variant, str) else variant['name']
            method_name = self._to_method_name(variant_name)
            if i == 0:
                lines.append(f'        if variant == "{variant_name}":')
            else:
                lines.append(f'        elif variant == "{variant_name}":')
            lines.append(f'            config = self.{method_name}(blueprint, difficulty)')
        lines.append('        else:')
        first_variant = variants[0] if isinstance(variants[0], str) else variants[0]['name']
        lines.append(f'            config = self.{self._to_method_name(first_variant)}(blueprint, difficulty)')
        return '\n'.join(lines)

    def _generate_template_dispatch(self, variants: list) -> str:
        """Generate if-elif chain for template dispatch"""
        lines = []
        for i, variant in enumerate(variants):
            variant_name = variant if isinstance(variant, str) else variant['name']
            method_name = self._to_method_name(variant_name)
            if i == 0:
                lines.append(f'        if variant == "{variant_name}":')
            else:
                lines.append(f'        elif variant == "{variant_name}":')
            lines.append(f'            return self.{method_name}()')
        lines.append('        else:')
        first_variant = variants[0] if isinstance(variants[0], str) else variants[0]['name']
        lines.append(f'            return self.{self._to_method_name(first_variant)}()')
        return '\n'.join(lines)

    def _generate_variant_method(self, variant: dict, method_name: str) -> str:
        """Generate a variant mutation method"""

        variant_name = variant['name']
        contexts = self.config.get('mutation_axes', {}).get('contexts', [])
        
        # Get contexts list
        if contexts and isinstance(contexts[0], dict):
            context_names = [c['name'] for c in contexts]
        else:
            context_names = contexts if contexts else ['default_context']

        return f'''    def {method_name}(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate {variant_name} vulnerability configuration"""

        contexts = {context_names}
        context = self.select_random(contexts)
        
        entry_points = blueprint.entry_points
        entry_point = self.select_random(entry_points)

        # Select filters based on difficulty
        if difficulty == 1:
            filters = []
        elif difficulty == 2:
            filters = self._get_filter_codes(['single_quote', 'or_keyword'])
        elif difficulty == 3:
            filters = self._get_filter_codes(['single_quote', 'or_keyword', 'union_keyword'])
        else:
            filters = self._get_filter_codes(['single_quote', 'or_keyword', 'union_keyword', 'select_keyword'])

        flag_content = self.generate_flag()
        hints = self._generate_hints(filters, context, difficulty)

        return {{
            'application': {{
                'context': context,
                'variant': '{variant_name}',
                'entry_point': entry_point,
            }},
            'constraints': {{
                'filters': filters,
            }},
            'flag': {{
                'content': flag_content,
                'location': '/var/www/html/flag.txt',
            }},
            'behavior': {{
                'output': 'direct_echo',
            }},
            'metadata': {{
                'exploit_hints': hints,
                'vulnerability_type': '{variant_name}',
                'estimated_solve_time': f"{{difficulty * 10}}-{{difficulty * 15}} minutes",
                'vuln_name': '{self.vuln_name}',
                'category': '{self.category}',
                'description': '{variant.get("description", "")}',
            }}
        }}
'''

    def _generate_template_method(self, variant: dict, method_name: str, needs_db: bool) -> str:
        """Generate a variant template method WITH THEME SUPPORT"""

        variant_name = variant['name']
        
        if needs_db:
            db_code = '''
        // Database connection
        $conn = mysqli_connect('db', 'hackforge', 'hackforge123', 'hackforge');
        if (!$conn) {{
            die("Connection failed: " . mysqli_connect_error());
        }}'''
            
            query_code = '''
            // Vulnerable SQL query
            $query = "SELECT * FROM users WHERE username='$input'";
            $result = mysqli_query($conn, $query);
            
            if ($result) {{
                echo '<div class="result">';
                echo '<h3>Results:</h3>';
                while ($row = mysqli_fetch_assoc($result)) {{
                    echo '<div>User: ' . $row['username'] . '</div>';
                }}
                echo '</div>';
            }} else {{
                echo '<div class="result error">Error: ' . mysqli_error($conn) . '</div>';
            }}
            
            mysqli_close($conn);'''
        else:
            db_code = ''
            query_code = '''
            echo '<div class="result">';
            echo '<h3>Results:</h3>';
            echo '<div>' . $input . '</div>';
            echo '</div>';'''

        return f'''    def {method_name}(self) -> str:
        """Generate {variant_name} vulnerable application with themed UI"""

        app = self.config.application
        constraints = self.config.constraints

        context = app.get('context', 'default')
        filters = constraints.get('filters', [])

        filter_code = self._generate_filter_code(filters, 'php')

        # Get theme CSS and properties
        theme_css = self.theme['css']
        fonts_import = self.theme.get('fonts_import', '')
        placeholder = self.theme.get('placeholder', 'Enter input')
        button_text = self.theme.get('button_text', 'Submit')

        php_code = f\'\'\'<?php
/**
 * Hackforge Machine: {{self.machine_id}}
 * Vulnerability: {variant_name}
 * Theme: {{self.theme['name']}}
 * Difficulty: {{self.difficulty}}/5
 */
{db_code}
?>
<!DOCTYPE html>
<html>
<head>
    <title>{variant_name} Challenge</title>
    {{fonts_import}}
    <style>
{{theme_css}}
    </style>
</head>
<body>
    <div class="container">
        <h1>{variant_name}</h1>
        <p>Context: {{context}}</p>

        <form method="GET">
            <input type="text" name="input" placeholder="{{placeholder}}">
            <button type="submit">{{button_text}}</button>
        </form>

        <?php
        if (isset($_GET['input'])) {{{{
            $input = $_GET['input'];
            {{filter_code if filter_code else '// No filters'}}
{query_code}
        }}}}
        ?>

        <div class="hint">
            <strong>💡 Hint:</strong> This is a {{context}} context. Can you find the vulnerability?
        </div>
    </div>
</body>
</html>\'\'\'

        return php_code
'''

    def _generate_filter_map(self) -> str:
        """Generate filter mapping code from new JSON structure"""
        filters = self.config.get('mutation_axes', {}).get('filters', {})

        filter_entries = []
        seen_filters = set()
        
        for category, filter_list in filters.items():
            if category in ['basic', 'medium', 'advanced']:
                for filter_obj in filter_list:
                    if isinstance(filter_obj, dict):
                        filter_name = filter_obj['name']
                        if filter_name not in seen_filters:
                            seen_filters.add(filter_name)
                            # Escape quotes properly for PHP and Python code
                            php_code = filter_obj.get('php_code', '').replace('"', '\\"').replace("'", "\\'")
                            python_code = filter_obj.get('python_code', '').replace('"', '\\"').replace("'", "\\'")
                            description = filter_obj.get('description', '').replace("'", "\\'")
                            
                            filter_entries.append(f"""            '{filter_name}': {{
                'type': '{filter_obj.get('type', filter_name)}',
                'description': '{description}',
                'php_code': '''{php_code}''',
                'python_code': '''{python_code}''',
            }}""")

        return ',\n'.join(filter_entries) if filter_entries else "            # No filters defined"

    def _generate_dockerfile_method(self) -> str:
        """Generate Dockerfile method based on infrastructure requirements"""
        
        infrastructure = self.config.get('infrastructure', {})
        needs_db = infrastructure.get('needs_database', False)
        docker_reqs = infrastructure.get('docker_requirements', {})
        
        base_image = docker_reqs.get('base_image', 'php:8.0-apache')
        extensions = docker_reqs.get('extensions', [])
        packages = docker_reqs.get('packages', [])
        
        # Build extension installation
        ext_install = ''
        if extensions:
            ext_install = f"docker-php-ext-install {' '.join(extensions)} && \\\\\n    "
        
        # Build package installation
        pkg_install = ''
        if packages:
            pkg_install = ' \\\\\n    '.join(packages) + ' \\\\'
        
        if needs_db:
            return f'''        return \'\'\'FROM {base_image}

RUN apt-get update && apt-get install -y \\\\
    {pkg_install}
    iputils-ping \\\\
    whois \\\\
    dnsutils \\\\
    && rm -rf /var/lib/apt/lists/* && \\\\
    {ext_install}rm -rf /tmp/*

EXPOSE 80

CMD ["apache2-foreground"]
\'\'\'
'''
        else:
            return '''        return \'\'\'FROM php:8.0-apache

RUN apt-get update && apt-get install -y \\\\
    iputils-ping \\\\
    whois \\\\
    dnsutils \\\\
    && rm -rf /var/lib/apt/lists/*

EXPOSE 80

CMD ["apache2-foreground"]
\'\'\'
'''


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python vuln_generator.py <config.json>")
        print("Example: python vuln_generator.py sqli_config.json")
        sys.exit(1)

    config_path = sys.argv[1]

    generator = VulnerabilityGenerator(config_path)
    generator.generate_all(".")

    print(f"\n✨ Done! Templates will now use random themes for variety!")
