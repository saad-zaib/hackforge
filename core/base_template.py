"""
AI-Enhanced Base Template
Modified base_template.py to use AI code generation
"""

import os
import sys
from pathlib import Path

# Add ai_code_generator to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_code_generator import AICodeGenerator, get_vuln_requirements


class AIEnhancedTemplate:
    """
    Base template that uses AI to generate vulnerable code
    """
    
    def __init__(self, config, use_ai: bool = True):
        self.config = config
        self.machine_id = config.machine_id
        self.difficulty = config.difficulty
        self.variant = config.variant
        self.category = config.blueprint_id.split('_')[0]  # e.g., "sql" from "sql_injection_001"
        
        self.use_ai = use_ai
        self.ai_generator = AICodeGenerator() if use_ai else None
        
        # Get vulnerability requirements
        self.vuln_reqs = get_vuln_requirements(self.category)
    
    def generate_code(self) -> str:
        """
        Generate vulnerable application code using AI
        """
        
        if not self.use_ai or not self.ai_generator:
            return self._generate_fallback_code()
        
        print(f"  🤖 Generating vulnerable code with AI...")
        
        # Extract config details
        app = self.config.application
        constraints = self.config.constraints
        context = app.get('context', 'default')
        filters = constraints.get('filters', [])
        
        # Generate vulnerable function
        vuln_function = self.ai_generator.generate_vulnerable_function(
            vuln_type=self.category.replace('_', ' ').title(),
            variant=self.variant,
            difficulty=self.difficulty,
            context=context,
            filters=filters
        )
        
        if not vuln_function:
            print("  ⚠️  AI generation failed, using fallback")
            return self._generate_fallback_code()
        
        # Wrap in minimal HTML
        return self._wrap_in_html(vuln_function, context)
    
    def _wrap_in_html(self, vuln_code: str, context: str) -> str:
        """
        Wrap vulnerable function in minimal HTML boilerplate
        """
        
        return f'''<?php
/**
 * Hackforge Machine: {self.machine_id}
 * Vulnerability: {self.variant}
 * Difficulty: {self.difficulty}/5
 */

{vuln_code}
?>
<!DOCTYPE html>
<html>
<head>
    <title>{self.variant} Challenge</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #1a1a1a;
            color: #fff;
        }}
        .container {{
            background: #2a2a2a;
            padding: 30px;
            border-radius: 8px;
        }}
        input, button {{
            padding: 10px;
            margin: 10px 0;
            font-size: 16px;
        }}
        input {{
            width: 100%;
            background: #333;
            border: 1px solid #555;
            color: #fff;
        }}
        button {{
            background: #e74c3c;
            color: white;
            border: none;
            cursor: pointer;
        }}
        .result {{
            margin-top: 20px;
            padding: 15px;
            background: #333;
            border-left: 4px solid #e74c3c;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{self.variant}</h1>
        <p>Context: {context}</p>
        
        <form method="GET">
            <input type="text" name="input" placeholder="Enter input">
            <button type="submit">Submit</button>
        </form>
        
        <?php
        // Call vulnerable function if input provided
        if (isset($_GET['input'])) {{
            // This is where the vulnerability is triggered
        }}
        ?>
    </div>
</body>
</html>'''
    
    def _generate_fallback_code(self) -> str:
        """
        Fallback if AI fails - basic template
        """
        
        return f'''<?php
/**
 * Hackforge Machine: {self.machine_id}
 * FALLBACK TEMPLATE - AI generation failed
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>Challenge</title>
</head>
<body>
    <h1>{self.variant}</h1>
    <form method="GET">
        <input name="input" placeholder="Input">
        <button>Submit</button>
    </form>
    <?php
    if (isset($_GET['input'])) {{
        echo htmlspecialchars($_GET['input']);
    }}
    ?>
</body>
</html>'''
    
    def generate_dockerfile(self) -> str:
        """
        Generate Dockerfile with AI additions if needed
        """
        
        base_dockerfile = '''FROM php:8.0-apache

RUN apt-get update && apt-get install -y \\
    iputils-ping \\
    whois \\
    dnsutils \\
    && rm -rf /var/lib/apt/lists/*

'''
        
        # Add AI-generated setup for specific vulnerabilities
        if self.use_ai and self.ai_generator:
            additions = self.ai_generator.generate_dockerfile_additions(
                vuln_type=self.category
            )
            
            if additions:
                base_dockerfile += additions + "\n\n"
        
        # Add database setup if needed
        if self.vuln_reqs.get('needs_db'):
            base_dockerfile += self._get_db_dockerfile_additions()
        
        base_dockerfile += '''
EXPOSE 80

CMD ["apache2-foreground"]
'''
        
        return base_dockerfile
    
    def _get_db_dockerfile_additions(self) -> str:
        """Database setup for SQLi/NoSQLi"""
        
        if 'sql' in self.category and 'nosql' not in self.category:
            return '''RUN docker-php-ext-install mysqli pdo pdo_mysql

'''
        elif 'nosql' in self.category:
            return '''RUN pecl install mongodb && docker-php-ext-enable mongodb

'''
        return ""
    
    def generate_docker_compose_service(self) -> Dict:
        """
        Generate docker-compose service definition
        """
        
        service = {
            'build': '.',
            'ports': ['80'],
            'volumes': [
                './app:/var/www/html',
                './flag.txt:/var/www/html/flag.txt:ro'
            ]
        }
        
        # Add database service if needed
        if self.vuln_reqs.get('needs_db'):
            service['depends_on'] = ['db']
        
        return service
    
    def generate_setup_files(self) -> Dict[str, str]:
        """
        Generate additional setup files (DB schema, file structure, etc.)
        
        Returns:
            Dict of {filename: content}
        """
        
        files = {}
        
        # Generate database schema if needed
        if self.vuln_reqs.get('needs_db') and self.use_ai:
            schema, docker = self.ai_generator.generate_database_setup(
                vuln_type=self.category,
                context=self.config.application.get('context', 'default'),
                flag=self.config.flag['content']
            )
            
            if schema:
                files['init.sql'] = schema
        
        # Generate file structure if needed
        if self.vuln_reqs.get('needs_files') and self.use_ai:
            file_structure = self.ai_generator.generate_file_structure(
                vuln_type=self.category,
                flag=self.config.flag['content']
            )
            
            if file_structure:
                files['setup_files.sh'] = self._generate_file_setup_script(file_structure)
        
        return files
    
    def _generate_file_setup_script(self, file_structure: Dict[str, str]) -> str:
        """
        Generate bash script to create file structure
        """
        
        script = "#!/bin/bash\n\n"
        script += "# Setup file structure for vulnerability\n\n"
        
        for filepath, content in file_structure.items():
            # Escape content for bash
            content_escaped = content.replace('"', '\\"').replace('$', '\\$')
            
            script += f'echo "{content_escaped}" > {filepath}\n'
            script += f'chmod 644 {filepath}\n\n'
        
        return script


# Test
if __name__ == "__main__":
    print("Testing AI-Enhanced Template...")
    
    # Mock config
    class MockConfig:
        machine_id = "test_123"
        difficulty = 3
        variant = "Error-based SQLi"
        blueprint_id = "sql_injection_001"
        application = {"context": "login system"}
        constraints = {"filters": []}
        flag = {"content": "FLAG{test}"}
    
    template = AIEnhancedTemplate(MockConfig(), use_ai=True)
    
    print("\n1. Generating code...")
    code = template.generate_code()
    print(code[:300] if code else "Failed")
    
    print("\n2. Generating Dockerfile...")
    dockerfile = template.generate_dockerfile()
    print(dockerfile[:200])
    
    print("\n3. Generating setup files...")
    files = template.generate_setup_files()
    print(f"Generated {len(files)} setup files")
