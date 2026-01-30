#!/usr/bin/env python3
"""
AI Code Generator - FIXED
Uses full blueprint config for enhanced AI generation
"""

import requests
import json
import re
from typing import Dict, Optional, List


class AICodeGenerator:
    """Calls AI API to generate vulnerable code components"""

    def __init__(self, api_url: str = "http://localhost:8080/v1/chat/completions"):
        self.api_url = api_url
        self.timeout = 60

    def _call_api(self, system_prompt: str, user_prompt: str, temperature: float = 0.7) -> Optional[str]:
        """Call AI API and return response"""
        payload = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature
        }

        try:
            response = requests.post(
                self.api_url,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()

            data = response.json()
            content = data['choices'][0]['message']['content']
            content = self._strip_markdown(content)
            return content

        except Exception as e:
            print(f"AI API Error: {e}")
            return None

    def _strip_markdown(self, text: str) -> str:
        """Remove markdown code fences"""
        text = re.sub(r'```[\w]*\n?', '', text)
        text = text.strip()
        return text

    def generate_vulnerable_function(self,
                                     blueprint_config: Dict,
                                     variant: Dict,
                                     difficulty: int,
                                     context: Dict,
                                     filters: List[Dict]) -> Optional[str]:
        """Generate vulnerable function using FULL blueprint config"""

        # Extract info from enhanced config
        vuln_name = blueprint_config.get('name', 'Unknown')
        category = blueprint_config.get('category', 'unknown')
        infrastructure = blueprint_config.get('infrastructure', {})
        ai_hints = blueprint_config.get('ai_generation_hints', {})

        # Build system prompt with AI hints
        system_prompt = f"""You are a security code generator. Generate ONLY vulnerable PHP code logic.

CRITICAL RULES:
- Output ONLY PHP code for the vulnerable function
- NO HTML, NO form handling, NO complete page
- NO markdown fences, NO explanations
- Just the vulnerable code block
- Maximum 30 lines of code
- Use proper PHP syntax

{ai_hints.get('code_structure', '')}
{ai_hints.get('vulnerability_placement', '')}
"""

        # Build filter description with bypass hints
        filter_desc = "No filtering"
        if filters:
            filter_lines = []
            for f in filters:
                filter_lines.append(f"  - {f['type']}: {f.get('description', '')}")
                # Get bypass hint from blueprint if available
                hint = f.get('bypass_hint', '')
                if hint:
                    filter_lines.append(f"    Bypass: {hint}")
            filter_desc = "Filters applied:\n" + "\n".join(filter_lines)

        # Build context info with query template
        context_name = context.get('name', 'default')
        query_template = context.get('query_template', '')
        context_desc = context.get('description', '')

        # Build user prompt
        user_prompt = f"""Generate vulnerable PHP code for {vuln_name}:

Variant: {variant.get('name', 'Basic')}
Description: {variant.get('description', '')}
Context: {context_name} - {context_desc}
Difficulty: {difficulty}/5

{filter_desc}

Exploit Example: {variant.get('exploit_example', 'N/A')}

Requirements:
1. Read input from $_GET['input']
2. Apply filters if specified
"""

        # Add specific requirements based on infrastructure
        if infrastructure.get('needs_database'):
            db_type = infrastructure.get('database_type', 'mysql')
            db_conn = ai_hints.get('database_connection', '')

            user_prompt += f"""3. Connect to {db_type} database: {db_conn}
4. Execute vulnerable query: {query_template}
5. Display results or error messages based on output_type: {variant.get('output_type', 'direct_output')}
"""
        else:
            user_prompt += f"""3. Execute vulnerable operation
4. Display output to user
"""

        user_prompt += f"""
Output format example:
$input = $_GET['input'];
// Apply filters
{filters[0]['php_code'] if filters else '// No filters'}
// Vulnerable operation
$result = vulnerable_function($input);
echo $result;
"""

        return self._call_api(system_prompt, user_prompt, temperature=0.7)

    def generate_dockerfile_additions(self, blueprint_config: Dict) -> str:
        """Generate Dockerfile additions from infrastructure config"""
        
        infrastructure = blueprint_config.get('infrastructure', {})
        docker_reqs = infrastructure.get('docker_requirements', {})
        
        additions = ""
        
        # Add extensions
        extensions = docker_reqs.get('extensions', [])
        if extensions:
            ext_list = ' '.join(extensions)
            additions += f"RUN docker-php-ext-install {ext_list}\n"
        
        # Add packages are handled in base dockerfile
        
        return additions

    def generate_database_setup(self, 
                                blueprint_config: Dict,
                                flag: str) -> tuple[str, str]:
        """Generate database setup from blueprint config"""
        
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
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: root123
      MONGO_INITDB_DATABASE: hackforge
    volumes:
      - ./init.js:/docker-entrypoint-initdb.d/init.js
      - mongo_data:/data/db
    restart: unless-stopped"""

    def generate_file_structure(self, blueprint_config: Dict, flag: str) -> Dict[str, str]:
        """Generate file structure if needed"""
        
        infrastructure = blueprint_config.get('infrastructure', {})
        
        if not infrastructure.get('needs_file_system'):
            return {}
        
        # Create basic file structure
        files = {
            '/var/www/config/flag.txt': flag,
            '/var/www/config/database.conf': 'DB_HOST=localhost',
            '/tmp/logs/access.log': 'Access log initialized',
        }
        
        return files


if __name__ == "__main__":
    print("Testing AI Code Generator...")

    # Load config
    with open('configs/sqli.json', 'r') as f:
        blueprint_config = json.load(f)

    print(f"✓ Loaded config: {blueprint_config['name']}")
    print(f"✓ Infrastructure: DB={blueprint_config['infrastructure']['needs_database']}")
    print(f"✓ Variants: {len(blueprint_config['variants'])}")
