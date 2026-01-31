#!/usr/bin/env python3
"""
AI Docker Generator - FIXED
Properly generates database services in docker-compose
AND strips markdown code fences from AI responses
"""

import requests
import json
import re
from typing import Dict, Optional, Tuple


class AIDockerGenerator:
    """Generates Docker infrastructure using enhanced config"""

    def __init__(self, api_url: str = "http://localhost:8080/v1/chat/completions"):
        self.api_url = api_url
        self.timeout = 60

    def _call_api(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """Call AI API"""
        try:
            response = requests.post(
                self.api_url,
                headers={"Content-Type": "application/json"},
                json={
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.5
                },
                timeout=self.timeout
            )
            response.raise_for_status()
            content = response.json()['choices'][0]['message']['content']
            return self._strip_markdown(content)
        except Exception as e:
            print(f"AI API Error: {e}")
            return None

    def _strip_markdown(self, text: str) -> str:
        """Remove markdown code fences and language identifiers"""
        # Remove code fences with optional language identifier (e.g., ```dockerfile or ```)
        text = re.sub(r'```[\w]*\n?', '', text)
        # Remove standalone "Dockerfile" or "dockerfile" on its own line at start
        text = re.sub(r'^[Dd]ockerfile\s*\n', '', text, flags=re.MULTILINE)
        return text.strip()

    def generate_dockerfile_from_config(self, blueprint_config: Dict) -> str:
        """Generate Dockerfile from enhanced config"""

        infrastructure = blueprint_config.get('infrastructure', {})
        docker_reqs = infrastructure.get('docker_requirements', {})
        ai_hints = blueprint_config.get('ai_generation_hints', {})

        base_image = docker_reqs.get('base_image', 'php:8.0-apache')
        extensions = docker_reqs.get('extensions', [])
        packages = docker_reqs.get('packages', [])

        system_prompt = """Generate a Dockerfile for vulnerable web applications.
Output ONLY the Dockerfile content, no explanations.
DO NOT include markdown code fences (```).
DO NOT include the word "Dockerfile" as a header."""

        user_prompt = f"""Create Dockerfile with these requirements:

Base Image: {base_image}
Extensions: {', '.join(extensions) if extensions else 'None'}
Packages: {', '.join(packages) if packages else 'Standard tools'}

{ai_hints.get('dockerfile_notes', '')}

Standard requirements:
- Install: iputils-ping, whois, dnsutils, net-tools, curl, wget
- Enable Apache mod_rewrite
- Expose port 80
- Keep under 25 lines

IMPORTANT: Use apt-get to install system packages (like mysqli, curl, wget)
Use docker-php-ext-install ONLY for PHP extensions (like pdo, pdo_mysql, mysqli)
DO NOT mix them up!

Output format (NO markdown fences, NO "Dockerfile" header):
FROM {base_image}
RUN apt-get update && apt-get install -y ...
...
CMD ["apache2-foreground"]
"""

        result = self._call_api(system_prompt, user_prompt)
        return result if result else self._fallback_dockerfile(infrastructure)

    def _fallback_dockerfile(self, infrastructure: Dict) -> str:
        """Fallback Dockerfile from infrastructure config"""

        docker_reqs = infrastructure.get('docker_requirements', {})
        base_image = docker_reqs.get('base_image', 'php:8.0-apache')
        extensions = docker_reqs.get('extensions', [])
        packages = docker_reqs.get('packages', [])

        dockerfile = f'''FROM {base_image}

RUN apt-get update && apt-get install -y \\
    iputils-ping \\
    whois \\
    dnsutils \\
    net-tools \\
    curl \\
    wget \\
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

    def generate_database_setup_from_config(self, blueprint_config: Dict, flag: str) -> Tuple[str, str]:
        """Generate database setup from enhanced config"""

        infrastructure = blueprint_config.get('infrastructure', {})
        db_schema = blueprint_config.get('database_schema', {})

        if not infrastructure.get('needs_database'):
            return "", ""

        db_type = infrastructure.get('database_type', 'mysql')

        if db_type == 'mysql':
            schema = self._generate_mysql_schema(db_schema, flag)
            compose = self._generate_mysql_compose()
            return schema, compose
        elif db_type == 'mongodb':
            schema = self._generate_mongodb_init(db_schema, flag)
            compose = self._generate_mongodb_compose()
            return schema, compose

        return "", ""

    def _generate_mysql_schema(self, schema_config: Dict, flag: str) -> str:
        """Generate MySQL schema from config"""
        sql = "CREATE DATABASE IF NOT EXISTS hackforge;\nUSE hackforge;\n\n"

        tables = schema_config.get('tables', [])
        for table in tables:
            table_name = table['name']
            columns = table['columns']

            sql += f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
            sql += "    " + ",\n    ".join(columns)
            sql += "\n);\n\n"

        # Insert seed data
        seed_data = schema_config.get('seed_data', {})

        for table_name, rows in seed_data.items():
            for row in rows:
                columns = list(row.keys())
                values = []
                for val in row.values():
                    if val == "{{FLAG}}":
                        values.append(f"'{flag}'")
                    elif val == "NOW()":
                        values.append("NOW()")
                    else:
                        values.append(f"'{val}'")

                sql += f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)});\n"

        sql += "\n"
        return sql

    def _generate_mongodb_init(self, schema_config: Dict, flag: str) -> str:
        """Generate MongoDB init script from config"""
        js = "db = db.getSiblingDB('hackforge');\n\n"

        tables = schema_config.get('tables', [])
        for table in tables:
            js += f"db.createCollection('{table['name']}');\n"

        js += "\n"

        seed_data = schema_config.get('seed_data', {})

        for collection, rows in seed_data.items():
            for row in rows:
                row_copy = row.copy()
                for k, v in row_copy.items():
                    if v == '{{FLAG}}':
                        row_copy[k] = flag

                js += f"db.{collection}.insertOne({json.dumps(row_copy)});\n"

        return js

    def _generate_mysql_compose(self) -> str:
        """Generate MySQL docker-compose service"""
        return """  db:
    image: mysql:8.0
    container_name: hackforge_db
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: hackforge
      MYSQL_USER: hackforge
      MYSQL_PASSWORD: hackforge123
    volumes:
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
      - db_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped"""

    def _generate_mongodb_compose(self) -> str:
        """Generate MongoDB docker-compose service"""
        return """  mongodb:
    image: mongo:5.0
    container_name: hackforge_mongodb
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: root123
      MONGO_INITDB_DATABASE: hackforge
    volumes:
      - ./init.js:/docker-entrypoint-initdb.d/init.js
      - mongo_data:/data/db
    restart: unless-stopped"""

    def generate_docker_compose(self, machines: list, blueprint_configs: Dict[str, Dict]) -> str:
        """FIXED: Generate master docker-compose.yml with proper database services"""

        compose = "version: '3.8'\n\nservices:\n"

        # First pass: Add web services
        for machine in machines:
            machine_id = machine['machine_id']
            port = machine.get('port', 8081)
            category = machine.get('category', '')

            # Find blueprint config
            blueprint_config = self._find_blueprint_config(category, blueprint_configs)
            infrastructure = blueprint_config.get('infrastructure', {}) if blueprint_config else {}

            compose += f"""
  {machine_id}:
    build: ./{machine_id}
    container_name: hackforge_{machine_id}
    ports:
      - "{port}:80"
    volumes:
      - ./{machine_id}/app:/var/www/html
"""

            # Add database dependency if needed
            if infrastructure.get('needs_database'):
                db_type = infrastructure.get('database_type', 'mysql')
                if db_type == 'mysql':
                    compose += f"    depends_on:\n      - db_{machine_id}\n"
                elif db_type == 'mongodb':
                    compose += f"    depends_on:\n      - mongodb_{machine_id}\n"

            compose += "    restart: unless-stopped\n"

        # Second pass: Add database services
        for machine in machines:
            machine_id = machine['machine_id']
            category = machine.get('category', '')

            # Find blueprint config
            blueprint_config = self._find_blueprint_config(category, blueprint_configs)
            infrastructure = blueprint_config.get('infrastructure', {}) if blueprint_config else {}

            if infrastructure.get('needs_database'):
                db_type = infrastructure.get('database_type', 'mysql')

                if db_type == 'mysql':
                    compose += f"""
  db_{machine_id}:
    image: mysql:8.0
    container_name: hackforge_db_{machine_id}
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: hackforge
      MYSQL_USER: hackforge
      MYSQL_PASSWORD: hackforge123
    volumes:
      - ./{machine_id}/init.sql:/docker-entrypoint-initdb.d/init.sql
      - db_data_{machine_id}:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
"""

                elif db_type == 'mongodb':
                    compose += f"""
  mongodb_{machine_id}:
    image: mongo:5.0
    container_name: hackforge_mongodb_{machine_id}
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: root123
    volumes:
      - ./{machine_id}/init.js:/docker-entrypoint-initdb.d/init.js
      - mongo_data_{machine_id}:/data/db
    restart: unless-stopped
"""

        # Add volumes section
        volumes_needed = set()
        for machine in machines:
            category = machine.get('category', '')
            blueprint_config = self._find_blueprint_config(category, blueprint_configs)
            infrastructure = blueprint_config.get('infrastructure', {}) if blueprint_config else {}

            if infrastructure.get('needs_database'):
                db_type = infrastructure.get('database_type', 'mysql')
                if db_type == 'mysql':
                    volumes_needed.add(f"db_data_{machine['machine_id']}")
                elif db_type == 'mongodb':
                    volumes_needed.add(f"mongo_data_{machine['machine_id']}")

        if volumes_needed:
            compose += "\nvolumes:\n"
            for vol in sorted(volumes_needed):
                compose += f"  {vol}:\n"

        return compose

    def _find_blueprint_config(self, category: str, blueprint_configs: Dict[str, Dict]) -> Dict:
        """FIXED: Find blueprint config with better matching"""
        
        # Direct match
        if category in blueprint_configs:
            return blueprint_configs[category]
        
        # Fuzzy match - try different variations
        for config_key, config in blueprint_configs.items():
            # Check if category is substring of config key
            if category in config_key or config_key in category:
                return config
            
            # Check if config's category matches
            if config.get('category') == category:
                return config
        
        # No match found
        return {}


if __name__ == "__main__":
    print("Testing AI Docker Generator...")

    # Load config
    with open('configs/sqli.json', 'r') as f:
        config = json.load(f)

    gen = AIDockerGenerator()

    print("\n1. Generating Dockerfile...")
    dockerfile = gen.generate_dockerfile_from_config(config)
    print(dockerfile[:200] if dockerfile else "Failed")

    print("\n2. Generating database setup...")
    schema, compose = gen.generate_database_setup_from_config(config, "FLAG{test}")
    print(f"Schema: {len(schema)} chars")
    print(f"Compose service generated: {'Yes' if compose else 'No'}")

    print("\n✓ Tests complete")
