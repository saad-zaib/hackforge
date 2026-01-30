"""
SQL Injection Vulnerability Templates
Generates vulnerable applications with theme variety
"""

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from base_template import BaseTemplate
from theme_library import ThemeLibrary
from typing import Dict


class SqlInjectionTemplate(BaseTemplate):
    """
    Template generator for sql injection vulnerabilities
    """

    def __init__(self, config):
        super().__init__(config)
        # Pick random theme for this machine
        self.theme_name, self.theme = ThemeLibrary.get_random_theme()
        print(f"  🎨 Theme: {self.theme['name']}")

    def generate_code(self) -> str:
        """Generate vulnerable application based on variant"""

        variant = self.config.variant

        if variant == "Error-based SQL Injection":
            return self._generate_error_based_sql_injection()
        elif variant == "Union-based SQL Injection":
            return self._generate_union_based_sql_injection()
        elif variant == "Blind SQL Injection":
            return self._generate_blind_sql_injection()
        else:
            return self._generate_error_based_sql_injection()

    def _generate_error_based_sql_injection(self) -> str:
        """Generate Error-based SQL Injection vulnerable application with themed UI"""

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

        php_code = f'''<?php
/**
 * Hackforge Machine: {self.machine_id}
 * Vulnerability: Error-based SQL Injection
 * Theme: {self.theme['name']}
 * Difficulty: {self.difficulty}/5
 */

        // Database connection
        $conn = mysqli_connect('db', 'hackforge', 'hackforge123', 'hackforge');
        if (!$conn) {{
            die("Connection failed: " . mysqli_connect_error());
        }}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Error-based SQL Injection Challenge</title>
    {fonts_import}
    <style>
{theme_css}
    </style>
</head>
<body>
    <div class="container">
        <h1>Error-based SQL Injection</h1>
        <p>Context: {context}</p>

        <form method="GET">
            <input type="text" name="input" placeholder="{placeholder}">
            <button type="submit">{button_text}</button>
        </form>

        <?php
        if (isset($_GET['input'])) {{
            $input = $_GET['input'];
            {filter_code if filter_code else '// No filters'}

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
            
            mysqli_close($conn);
        }}
        ?>

        <div class="hint">
            <strong>💡 Hint:</strong> This is a {context} context. Can you find the vulnerability?
        </div>
    </div>
</body>
</html>'''

        return php_code

    def _generate_union_based_sql_injection(self) -> str:
        """Generate Union-based SQL Injection vulnerable application with themed UI"""

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

        php_code = f'''<?php
/**
 * Hackforge Machine: {self.machine_id}
 * Vulnerability: Union-based SQL Injection
 * Theme: {self.theme['name']}
 * Difficulty: {self.difficulty}/5
 */

        // Database connection
        $conn = mysqli_connect('db', 'hackforge', 'hackforge123', 'hackforge');
        if (!$conn) {{
            die("Connection failed: " . mysqli_connect_error());
        }}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Union-based SQL Injection Challenge</title>
    {fonts_import}
    <style>
{theme_css}
    </style>
</head>
<body>
    <div class="container">
        <h1>Union-based SQL Injection</h1>
        <p>Context: {context}</p>

        <form method="GET">
            <input type="text" name="input" placeholder="{placeholder}">
            <button type="submit">{button_text}</button>
        </form>

        <?php
        if (isset($_GET['input'])) {{
            $input = $_GET['input'];
            {filter_code if filter_code else '// No filters'}

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
            
            mysqli_close($conn);
        }}
        ?>

        <div class="hint">
            <strong>💡 Hint:</strong> This is a {context} context. Can you find the vulnerability?
        </div>
    </div>
</body>
</html>'''

        return php_code

    def _generate_blind_sql_injection(self) -> str:
        """Generate Blind SQL Injection vulnerable application with themed UI"""

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

        php_code = f'''<?php
/**
 * Hackforge Machine: {self.machine_id}
 * Vulnerability: Blind SQL Injection
 * Theme: {self.theme['name']}
 * Difficulty: {self.difficulty}/5
 */

        // Database connection
        $conn = mysqli_connect('db', 'hackforge', 'hackforge123', 'hackforge');
        if (!$conn) {{
            die("Connection failed: " . mysqli_connect_error());
        }}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Blind SQL Injection Challenge</title>
    {fonts_import}
    <style>
{theme_css}
    </style>
</head>
<body>
    <div class="container">
        <h1>Blind SQL Injection</h1>
        <p>Context: {context}</p>

        <form method="GET">
            <input type="text" name="input" placeholder="{placeholder}">
            <button type="submit">{button_text}</button>
        </form>

        <?php
        if (isset($_GET['input'])) {{
            $input = $_GET['input'];
            {filter_code if filter_code else '// No filters'}

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
            
            mysqli_close($conn);
        }}
        ?>

        <div class="hint">
            <strong>💡 Hint:</strong> This is a {context} context. Can you find the vulnerability?
        </div>
    </div>
</body>
</html>'''

        return php_code


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
        """Generate Dockerfile for sql injection vulnerabilities"""

        return '''FROM php:8.0-apache

RUN apt-get update && apt-get install -y \\
    default-mysql-client \\
    iputils-ping \\
    whois \\
    dnsutils \\
    && rm -rf /var/lib/apt/lists/* && \\
    docker-php-ext-install mysqli pdo pdo_mysql && \\
    rm -rf /tmp/*

EXPOSE 80

CMD ["apache2-foreground"]
'''

