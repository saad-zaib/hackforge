"""
Command Injection Vulnerability Templates
Generates vulnerable applications with theme variety
"""

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from base_template import BaseTemplate
from theme_library import ThemeLibrary
from typing import Dict


class CommandInjectionTemplate(BaseTemplate):
    """
    Template generator for command injection vulnerabilities
    """

    def __init__(self, config):
        super().__init__(config)
        # Pick random theme for this machine
        self.theme_name, self.theme = ThemeLibrary.get_random_theme()
        print(f"  🎨 Theme: {self.theme['name']}")

    def generate_code(self) -> str:
        """Generate vulnerable application based on variant"""

        variant = self.config.variant

        if variant == "Basic Command Injection":
            return self._generate_basic_command_injection()
        elif variant == "Blind Command Injection":
            return self._generate_blind_command_injection()
        elif variant == "Time-based Command Injection":
            return self._generate_time_based_command_injection()
        else:
            return self._generate_basic_command_injection()

    def _generate_basic_command_injection(self) -> str:
        """Generate Basic Command Injection vulnerable application with themed UI"""

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
 * Vulnerability: Basic Command Injection
 * Theme: {self.theme['name']}
 * Difficulty: {self.difficulty}/5
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>Basic Command Injection Challenge</title>
    {fonts_import}
    <style>
{theme_css}
    </style>
</head>
<body>
    <div class="container">
        <h1>Basic Command Injection</h1>
        <p>Context: {context}</p>

        <form method="GET">
            <input type="text" name="input" placeholder="{placeholder}">
            <button type="submit">{button_text}</button>
        </form>

        <?php
        if (isset($_GET['input'])) {{
            $input = $_GET['input'];
            {filter_code if filter_code else '// No filters'}
            echo '<div class="result">';
            echo '<h3>Results:</h3>';
            echo '<div>' . $input . '</div>';
            echo '</div>';
        }}
        ?>

        <div class="hint">
            <strong>💡 Hint:</strong> This is a {context} context. Can you find the vulnerability?
        </div>
    </div>
</body>
</html>'''

        return php_code

    def _generate_blind_command_injection(self) -> str:
        """Generate Blind Command Injection vulnerable application with themed UI"""

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
 * Vulnerability: Blind Command Injection
 * Theme: {self.theme['name']}
 * Difficulty: {self.difficulty}/5
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>Blind Command Injection Challenge</title>
    {fonts_import}
    <style>
{theme_css}
    </style>
</head>
<body>
    <div class="container">
        <h1>Blind Command Injection</h1>
        <p>Context: {context}</p>

        <form method="GET">
            <input type="text" name="input" placeholder="{placeholder}">
            <button type="submit">{button_text}</button>
        </form>

        <?php
        if (isset($_GET['input'])) {{
            $input = $_GET['input'];
            {filter_code if filter_code else '// No filters'}
            echo '<div class="result">';
            echo '<h3>Results:</h3>';
            echo '<div>' . $input . '</div>';
            echo '</div>';
        }}
        ?>

        <div class="hint">
            <strong>💡 Hint:</strong> This is a {context} context. Can you find the vulnerability?
        </div>
    </div>
</body>
</html>'''

        return php_code

    def _generate_time_based_command_injection(self) -> str:
        """Generate Time-based Command Injection vulnerable application with themed UI"""

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
 * Vulnerability: Time-based Command Injection
 * Theme: {self.theme['name']}
 * Difficulty: {self.difficulty}/5
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>Time-based Command Injection Challenge</title>
    {fonts_import}
    <style>
{theme_css}
    </style>
</head>
<body>
    <div class="container">
        <h1>Time-based Command Injection</h1>
        <p>Context: {context}</p>

        <form method="GET">
            <input type="text" name="input" placeholder="{placeholder}">
            <button type="submit">{button_text}</button>
        </form>

        <?php
        if (isset($_GET['input'])) {{
            $input = $_GET['input'];
            {filter_code if filter_code else '// No filters'}
            echo '<div class="result">';
            echo '<h3>Results:</h3>';
            echo '<div>' . $input . '</div>';
            echo '</div>';
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
        """Generate Dockerfile for command injection vulnerabilities"""

        return '''FROM php:8.0-apache

RUN apt-get update && apt-get install -y \\
    iputils-ping \\
    whois \\
    dnsutils \\
    && rm -rf /var/lib/apt/lists/*

EXPOSE 80

CMD ["apache2-foreground"]
'''
