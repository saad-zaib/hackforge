"""
Injection Vulnerability Templates
Generates vulnerable applications for injection attacks
"""

import os
import sys

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from templates.base_template import BaseTemplate
from typing import Dict


class InjectionTemplate(BaseTemplate):
    """
    Template generator for injection vulnerabilities
    """
    
    def generate_code(self) -> str:
        """Generate vulnerable application based on variant"""
        
        variant = self.config.variant
        
        if variant == "SQL Injection":
            return self._generate_sql_injection()
        elif variant == "Command Injection":
            return self._generate_command_injection()
        elif variant == "NoSQL Injection":
            return self._generate_nosql_injection()
        elif variant == "LDAP Injection":
            return self._generate_ldap_injection()
        elif variant == "Template Injection":
            return self._generate_template_injection()
        else:
            return self._generate_command_injection()
    
    def _generate_command_injection(self) -> str:
        """Generate command injection vulnerable PHP app"""
        
        app = self.config.application
        constraints = self.config.constraints
        behavior = self.config.behavior
        
        context = app['context']
        base_cmd = app['base_command']
        param_name = app['param_name']
        filters = constraints.get('filters', [])
        output_type = behavior['output']
        
        # Generate filter code
        filter_code = self._generate_filter_code(filters, 'php')
        
        # Generate output code - always show readable output
        output_code = 'echo htmlspecialchars($output);'
        
        php_code = f'''<?php
/**
 * Hackforge Machine: {self.machine_id}
 * Vulnerability: {self.variant}
 * Context: {context}
 * Difficulty: {self.difficulty}/5
 * 
 * EDUCATIONAL PURPOSE ONLY
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>{context.upper().replace('_', ' ')} Tool</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 50px auto;
            background: rgba(15, 32, 39, 0.9);
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 255, 136, 0.2);
            border: 1px solid rgba(0, 255, 136, 0.3);
        }}
        h1 {{
            color: #00ff88;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
        }}
        .subtitle {{
            color: #888;
            font-size: 0.9em;
            margin-bottom: 30px;
        }}
        .info-box {{
            background: rgba(0, 255, 136, 0.1);
            border-left: 4px solid #00ff88;
            padding: 15px;
            margin-bottom: 25px;
            border-radius: 5px;
        }}
        .info-box strong {{ color: #00ff88; }}
        .form-group {{
            margin: 25px 0;
        }}
        label {{
            display: block;
            color: #00ff88;
            margin-bottom: 10px;
            font-weight: bold;
        }}
        input[type="text"] {{
            width: 100%;
            padding: 15px;
            background: rgba(0, 0, 0, 0.4);
            border: 2px solid #00ff88;
            border-radius: 8px;
            color: #fff;
            font-size: 1em;
            font-family: 'Courier New', monospace;
            transition: all 0.3s;
        }}
        input[type="text"]:focus {{
            outline: none;
            border-color: #00ffff;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
        }}
        button {{
            background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%);
            color: #000;
            border: none;
            padding: 15px 40px;
            font-size: 1.1em;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-right: 10px;
        }}
        button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0, 255, 136, 0.4);
        }}
        .clear-btn {{
            background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%);
            color: #fff;
        }}
        .examples {{
            background: rgba(0, 255, 136, 0.05);
            border: 1px solid rgba(0, 255, 136, 0.2);
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
        }}
        .examples h3 {{
            color: #00ff88;
            font-size: 1em;
            margin-bottom: 10px;
        }}
        .example-cmd {{
            background: rgba(0, 0, 0, 0.4);
            padding: 8px 12px;
            margin: 5px 0;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            cursor: pointer;
            transition: all 0.2s;
            display: inline-block;
            color: #0ff;
        }}
        .example-cmd:hover {{
            background: rgba(0, 255, 136, 0.2);
            transform: translateX(5px);
        }}
        .output {{
            background: rgba(0, 0, 0, 0.6);
            border: 2px solid #00ff88;
            border-radius: 8px;
            padding: 20px;
            margin-top: 25px;
            min-height: 150px;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            color: #0f0;
            overflow-x: auto;
            line-height: 1.6;
        }}
        .hint {{
            color: #666;
            font-size: 0.85em;
            margin-top: 20px;
            text-align: center;
        }}
        .filters {{
            background: rgba(255, 0, 0, 0.1);
            border-left: 4px solid #ff4444;
            padding: 10px;
            margin: 15px 0;
            border-radius: 5px;
            font-size: 0.9em;
        }}
    </style>
    <script>
        function fillExample(cmd) {{
            document.getElementById('{param_name}').value = cmd;
        }}
        function clearOutput() {{
            window.location.href = window.location.pathname;
        }}
    </script>
</head>
<body>
    <div class="container">
        <h1>🔧 {context.upper().replace('_', ' ')}</h1>
        <div class="subtitle">Network Diagnostic Tool</div>
        
        <div class="info-box">
            <strong>Machine ID:</strong> <code>{self.machine_id}</code><br>
            <strong>Difficulty:</strong> {self.difficulty}/5<br>
            <strong>Parameter:</strong> <code>{param_name}</code>
        </div>
        
        {'<div class="filters">⚠️ Security Filters Active: ' + ', '.join([f['type'] for f in filters]) + '</div>' if filters else ''}
        
        <div class="examples">
            <h3>💡 Try These Examples:</h3>
            <div class="example-cmd" onclick="fillExample('google.com')">📍 google.com</div>
            <div class="example-cmd" onclick="fillExample('8.8.8.8')">📍 8.8.8.8</div>
            <div class="example-cmd" onclick="fillExample('localhost')">📍 localhost</div>
        </div>
        
        <form method="GET">
            <div class="form-group">
                <label for="{param_name}">Enter {param_name}:</label>
                <input type="text" 
                       id="{param_name}" 
                       name="{param_name}" 
                       placeholder="e.g., google.com, 8.8.8.8"
                       value="<?php echo htmlspecialchars($_GET['{param_name}'] ?? ''); ?>"
                       autofocus>
            </div>
            <button type="submit">▶ Execute Command</button>
            <button type="button" class="clear-btn" onclick="clearOutput()">🔄 Clear</button>
        </form>
        
        <?php
        if (isset($_GET['{param_name}'])) {{
            echo '<div class="output">';
            echo "<strong>⚡ Executing command...</strong>\\n\\n";
            
            $input = $_GET['{param_name}'];
            
            // Security filters (bypassable)
            {filter_code if filter_code else '// No filters applied'}
            
            // Execute command
            $command = "{base_cmd} " . $input . " 2>&1";
            $output = shell_exec($command);
            
            if ($output) {{
                {output_code}
            }} else {{
                echo "No output returned.";
            }}
            
            echo '</div>';
        }}
        ?>
        
        <div class="hint">
            💡 Can you find the flag? Try exploring the system...
        </div>
    </div>
</body>
</html>'''
        
        return php_code
    
    def _generate_sql_injection(self) -> str:
        """Generate SQL injection vulnerable PHP app"""
        
        app = self.config.application
        constraints = self.config.constraints
        behavior = self.config.behavior
        
        context = app['context']
        param_name = app['param_name']
        filters = constraints.get('filters', [])
        database = constraints['database']
        base_query = constraints['base_query']
        
        filter_code = self._generate_filter_code(filters, 'php')
        
        # Database connection based on type
        if database == 'mysql':
            db_setup = '''
    $conn = new mysqli("localhost", "root", "password", "hackforge");
    if ($conn->connect_error) {
        die("Connection failed");
    }'''
            query_code = '''
    $query = "''' + base_query.replace('{input}', '" . $input . "') + '''";
    $result = $conn->query($query);
    
    if ($result) {
        if ($result->num_rows > 0) {
            while($row = $result->fetch_assoc()) {
                foreach($row as $key => $value) {
                    echo htmlspecialchars($key) . ": " . htmlspecialchars($value) . "\\n";
                }
                echo "---\\n";
            }
        } else {
            echo "No results found.";
        }
    } else {
        if ($conn->error) {
            echo "Error: " . htmlspecialchars($conn->error);
        }
    }'''
        else:
            db_setup = '''
    $db = new SQLite3('/tmp/hackforge.db');'''
            query_code = '''
    $query = "''' + base_query.replace('{input}', '" . $input . "') + '''";
    $result = $db->query($query);
    
    if ($result) {
        while($row = $result->fetchArray(SQLITE3_ASSOC)) {
            foreach($row as $key => $value) {
                echo htmlspecialchars($key) . ": " . htmlspecialchars($value) . "\\n";
            }
            echo "---\\n";
        }
    } else {
        echo "Error: " . $db->lastErrorMsg();
    }'''
        
        php_code = f'''<?php
/**
 * Hackforge Machine: {self.machine_id}
 * Vulnerability: SQL Injection
 * Context: {context}
 * Database: {database}
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>{context.upper().replace('_', ' ')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #2c1e4e 0%, #1a1a3e 100%);
            color: #eee;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 50px auto;
            background: rgba(20, 20, 40, 0.9);
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(138, 43, 226, 0.3);
            border: 1px solid rgba(138, 43, 226, 0.4);
        }}
        h1 {{
            color: #9370db;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 0 0 10px rgba(147, 112, 219, 0.5);
        }}
        .info-box {{
            background: rgba(138, 43, 226, 0.1);
            border-left: 4px solid #9370db;
            padding: 15px;
            margin-bottom: 25px;
            border-radius: 5px;
        }}
        .info-box strong {{ color: #9370db; }}
        input[type="text"] {{
            width: 100%;
            padding: 15px;
            background: rgba(0, 0, 0, 0.4);
            border: 2px solid #9370db;
            border-radius: 8px;
            color: #fff;
            font-size: 1em;
            font-family: 'Courier New', monospace;
            margin: 15px 0;
        }}
        button {{
            background: linear-gradient(135deg, #9370db 0%, #7b68ee 100%);
            color: #fff;
            border: none;
            padding: 15px 40px;
            font-size: 1.1em;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
        }}
        button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(147, 112, 219, 0.4);
        }}
        .output {{
            background: rgba(0, 0, 0, 0.6);
            border: 2px solid #9370db;
            border-radius: 8px;
            padding: 20px;
            margin-top: 25px;
            min-height: 150px;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            color: #dda0dd;
        }}
        .filters {{
            background: rgba(255, 0, 0, 0.1);
            border-left: 4px solid #ff4444;
            padding: 10px;
            margin: 15px 0;
            border-radius: 5px;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🗄️ {context.upper().replace('_', ' ')}</h1>
        
        <div class="info-box">
            <strong>Machine ID:</strong> <code>{self.machine_id}</code><br>
            <strong>Database:</strong> {database}<br>
            <strong>Parameter:</strong> <code>{param_name}</code>
        </div>
        
        {'<div class="filters">⚠️ Security Filters Active: ' + ', '.join([f['type'] for f in filters]) + '</div>' if filters else ''}
        
        <form method="GET">
            <input type="text" 
                   name="{param_name}" 
                   placeholder="Enter {param_name}"
                   value="<?php echo htmlspecialchars($_GET['{param_name}'] ?? ''); ?>"
                   autofocus>
            <button type="submit">🔍 Search</button>
        </form>
        
        <?php
        if (isset($_GET['{param_name}'])) {{
            echo '<div class="output">';
            echo "<strong>Query Results:</strong>\\n\\n";
            
            $input = $_GET['{param_name}'];
            
            // Security filters
            {filter_code if filter_code else '// No filters'}
            
            // Database query
            {db_setup}
            {query_code}
            
            echo '</div>';
        }}
        ?>
    </div>
</body>
</html>'''
        
        return php_code
    

    def _generate_nosql_injection(self) -> str:
        """Generate NoSQL injection vulnerable PHP app with MongoDB"""

        app = self.config.application
        param_name = app.get('param_name', 'username')

        # Use PHP with MongoDB extension instead of Node.js
        php_code = f'''<?php
/**
 * Hackforge Machine: {self.machine_id}
 * Vulnerability: NoSQL Injection
 * Database: MongoDB
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>NoSQL User Search</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 50px auto;
            background: rgba(15, 32, 39, 0.9);
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 255, 136, 0.2);
        }}
        h1 {{
            color: #00ff88;
            font-size: 2.5em;
            margin-bottom: 30px;
        }}
        input[type="text"] {{
            width: 100%;
            padding: 15px;
            background: rgba(0, 0, 0, 0.4);
            border: 2px solid #00ff88;
            border-radius: 8px;
            color: #fff;
            font-size: 1em;
            margin: 15px 0;
        }}
        button {{
            background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%);
            color: #000;
            border: none;
            padding: 15px 40px;
            font-size: 1.1em;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
        }}
        .output {{
            background: rgba(0, 0, 0, 0.6);
            border: 2px solid #00ff88;
            border-radius: 8px;
            padding: 20px;
            margin-top: 25px;
            min-height: 150px;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            color: #0f0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 User Search</h1>

        <form method="GET">
            <input type="text"
                   name="{param_name}"
                   placeholder="Enter username"
                   value="<?php echo htmlspecialchars($_GET['{param_name}'] ?? ''); ?>"
                   autofocus>
            <button type="submit">Search</button>
        </form>

        <?php
        if (isset($_GET['{param_name}'])) {{
            echo '<div class="output">';
            echo "<strong>Search Results:</strong>\\n\\n";

            $input = $_GET['{param_name}'];

            try {{
                // Connect to MongoDB
                $manager = new MongoDB\\Driver\\Manager("mongodb://localhost:27017");

                // Vulnerable query - accepts array input for NoSQL injection
                $filter = ['{param_name}' => $input];
                $query = new MongoDB\\Driver\\Query($filter);

                $cursor = $manager->executeQuery("hackforge.users", $query);

                foreach ($cursor as $document) {{
                    echo "Username: " . htmlspecialchars($document->username) . "\\n";
                    echo "Email: " . htmlspecialchars($document->email) . "\\n";
                    echo "---\\n";
                }}
            }} catch (Exception $e) {{
                echo "Error: " . htmlspecialchars($e->getMessage());
            }}

            echo '</div>';
        }}
        ?>
    </div>
</body>
</html>'''

        return php_code

    
    def _generate_ldap_injection(self) -> str:
        """Generate LDAP injection vulnerable PHP app"""
        return "<!-- LDAP Injection template - similar structure -->"
    
    def _generate_template_injection(self) -> str:
        """Generate template injection vulnerable Python/Flask app"""
        return "# Template Injection - Python Flask app"
    
    def _generate_filter_code(self, filters: list, language: str) -> str:
        """Generate filter code from filter list"""
        if not filters:
            return ""
        
        if language == 'php':
            return "\n            ".join([f['php_code'] for f in filters])
        elif language == 'python':
            return "\n    ".join([f['python_code'] for f in filters])
        
        return ""
    
    def generate_dockerfile(self) -> str:
        """Generate Dockerfile for injection vulnerabilities"""
        
        variant = self.config.variant
        
        if variant in ["SQL Injection", "Command Injection"]:
            return '''FROM php:8.0-apache

# Install system tools
RUN apt-get update && apt-get install -y \\
    iputils-ping \\
    whois \\
    dnsutils \\
    default-mysql-client \\
    sqlite3 \\
    && rm -rf /var/lib/apt/lists/*

# Enable Apache modules
RUN a2enmod rewrite

# Set permissions
RUN chown -R www-data:www-data /var/www/html

EXPOSE 80

CMD ["apache2-foreground"]
'''
        elif variant == "NoSQL Injection":
            return '''FROM node:16

WORKDIR /app

RUN npm install express mongodb

COPY app /app

EXPOSE 3000

CMD ["node", "app.js"]
'''
        else:
            return '''FROM php:8.0-apache

RUN apt-get update && apt-get install -y iputils-ping whois dnsutils

EXPOSE 80

CMD ["apache2-foreground"]
'''
