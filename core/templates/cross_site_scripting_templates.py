"""
Cross-Site Scripting Vulnerability Templates
Generates vulnerable applications for cross-site scripting
"""

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from templates.base_template import BaseTemplate
from typing import Dict


class CrossSiteScriptingTemplate(BaseTemplate):
    """
    Template generator for cross-site scripting vulnerabilities
    """

    def generate_code(self) -> str:
        """Generate vulnerable application based on variant"""

        variant = self.config.variant

        if variant == "Reflected XSS":
            return self._generate_reflected_xss()
        elif variant == "Stored XSS":
            return self._generate_stored_xss()
        elif variant == "DOM-based XSS":
            return self._generate_dom_based_xss()
        else:
            return self._generate_reflected_xss()

    def _generate_reflected_xss(self) -> str:
        """Generate Reflected XSS vulnerable application"""

        app = self.config.application
        constraints = self.config.constraints

        context = app.get('context', 'default')
        filters = constraints.get('filters', [])

        filter_code = self._generate_filter_code(filters, 'php')

        # IMPORTANT: Double all curly braces {{}} to escape them in f-string
        php_code = f'''<?php
/**
 * Hackforge Machine: {self.machine_id}
 * Vulnerability: Reflected XSS
 * Context: {context}
 * Difficulty: {self.difficulty}/5
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>Reflected XSS Challenge</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
            padding: 20px;
            margin: 0;
        }}
        .container {{
            max-width: 900px;
            margin: 50px auto;
            background: rgba(15, 32, 39, 0.9);
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(0, 255, 136, 0.1);
        }}
        h1 {{
            color: #00ff88;
            text-align: center;
            margin-bottom: 30px;
        }}
        input {{
            width: 100%;
            padding: 15px;
            background: rgba(0, 0, 0, 0.4);
            border: 2px solid #00ff88;
            color: #fff;
            font-size: 16px;
            border-radius: 5px;
            margin-bottom: 15px;
            box-sizing: border-box;
        }}
        button {{
            background: #00ff88;
            color: #000;
            padding: 15px 40px;
            border: none;
            cursor: pointer;
            font-weight: bold;
            border-radius: 5px;
            width: 100%;
        }}
        button:hover {{
            background: #00cc6a;
        }}
        .result {{
            margin-top: 30px;
            padding: 20px;
            background: rgba(0, 0, 0, 0.3);
            border-left: 4px solid #00ff88;
            border-radius: 5px;
        }}
        .hint {{
            margin-top: 20px;
            padding: 15px;
            background: rgba(255, 193, 7, 0.1);
            border-left: 4px solid #ffc107;
            border-radius: 5px;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Search Portal</h1>
        <p style="text-align: center; color: #888;">Enter your search query below</p>
        
        <form method="GET">
            <input type="text" name="input" placeholder="Search for anything..." value="<?php echo isset($_GET['input']) ? $_GET['input'] : ''; ?>">
            <button type="submit">Search</button>
        </form>

        <?php
        if (isset($_GET['input'])) {{
            $input = $_GET['input'];
            
            {filter_code if filter_code else '// No input filtering applied'}
            
            echo '<div class="result">';
            echo '<h3>Search Results for: ' . $input . '</h3>';
            echo '<p>Showing results for your query...</p>';
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

    def _generate_stored_xss(self) -> str:
        """Generate Stored XSS vulnerable application"""

        app = self.config.application
        constraints = self.config.constraints

        context = app.get('context', 'default')
        filters = constraints.get('filters', [])

        filter_code = self._generate_filter_code(filters, 'php')

        # IMPORTANT: Double all curly braces {{}} to escape them in f-string
        php_code = f'''<?php
/**
 * Hackforge Machine: {self.machine_id}
 * Vulnerability: Stored XSS
 * Context: {context}
 * Difficulty: {self.difficulty}/5
 */

session_start();

// Simple in-memory storage (using session)
if (!isset($_SESSION['comments'])) {{
    $_SESSION['comments'] = array();
}}

// Handle new comment
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['comment'])) {{
    $comment = $_POST['comment'];
    
    {filter_code if filter_code else '// No input filtering applied'}
    
    $_SESSION['comments'][] = array(
        'text' => $comment,
        'time' => date('Y-m-d H:i:s')
    );
}}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Stored XSS Challenge</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
            padding: 20px;
            margin: 0;
        }}
        .container {{
            max-width: 900px;
            margin: 50px auto;
            background: rgba(15, 32, 39, 0.9);
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(0, 255, 136, 0.1);
        }}
        h1 {{
            color: #00ff88;
            text-align: center;
        }}
        h2 {{
            color: #00ff88;
            margin-top: 40px;
        }}
        textarea {{
            width: 100%;
            padding: 15px;
            background: rgba(0, 0, 0, 0.4);
            border: 2px solid #00ff88;
            color: #fff;
            font-size: 16px;
            border-radius: 5px;
            margin-bottom: 15px;
            font-family: inherit;
            box-sizing: border-box;
        }}
        button {{
            background: #00ff88;
            color: #000;
            padding: 15px 40px;
            border: none;
            cursor: pointer;
            font-weight: bold;
            border-radius: 5px;
        }}
        button:hover {{
            background: #00cc6a;
        }}
        .comment {{
            background: rgba(0, 0, 0, 0.3);
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #00ff88;
            border-radius: 5px;
        }}
        .comment-time {{
            color: #888;
            font-size: 12px;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>💬 Comment Board</h1>
        <p style="text-align: center; color: #888;">Share your thoughts</p>
        
        <form method="POST">
            <textarea name="comment" rows="4" placeholder="Leave a comment..."></textarea>
            <button type="submit">Post Comment</button>
        </form>
        
        <h2>Recent Comments</h2>
        
        <?php
        if (!empty($_SESSION['comments'])) {{
            foreach (array_reverse($_SESSION['comments']) as $comment) {{
                echo '<div class="comment">';
                echo '<div>' . $comment['text'] . '</div>';
                echo '<div class="comment-time">' . $comment['time'] . '</div>';
                echo '</div>';
            }}
        }} else {{
            echo '<p style="color: #888;">No comments yet. Be the first to comment!</p>';
        }}
        ?>
    </div>
</body>
</html>'''

        return php_code

    def _generate_dom_based_xss(self) -> str:
        """Generate DOM-based XSS vulnerable application"""

        app = self.config.application
        constraints = self.config.constraints

        context = app.get('context', 'default')
        filters = constraints.get('filters', [])

        filter_code = self._generate_filter_code(filters, 'php')

        # IMPORTANT: Double all curly braces {{}} to escape them in f-string
        php_code = f'''<?php
/**
 * Hackforge Machine: {self.machine_id}
 * Vulnerability: DOM-based XSS
 * Context: {context}
 * Difficulty: {self.difficulty}/5
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>DOM-based XSS Challenge</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
            padding: 20px;
            margin: 0;
        }}
        .container {{
            max-width: 900px;
            margin: 50px auto;
            background: rgba(15, 32, 39, 0.9);
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(0, 255, 136, 0.1);
        }}
        h1 {{
            color: #00ff88;
            text-align: center;
        }}
        #output {{
            margin-top: 30px;
            padding: 20px;
            background: rgba(0, 0, 0, 0.3);
            border-left: 4px solid #00ff88;
            border-radius: 5px;
            min-height: 50px;
        }}
        .hint {{
            margin-top: 20px;
            padding: 15px;
            background: rgba(255, 193, 7, 0.1);
            border-left: 4px solid #ffc107;
            border-radius: 5px;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>👤 User Profile</h1>
        <p style="text-align: center; color: #888;">Your profile information will be displayed below</p>
        
        <div id="output"></div>
        
        <div class="hint">
            <strong>💡 Hint:</strong> Check the URL fragment (#) for DOM-based XSS opportunities!
        </div>
    </div>
    
    <script>
        // Vulnerable DOM manipulation
        var hash = window.location.hash.substring(1);
        if (hash) {{
            document.getElementById('output').innerHTML = '<h3>Welcome, ' + hash + '!</h3>';
        }} else {{
            document.getElementById('output').innerHTML = '<p style="color: #888;">No user specified. Add #username to URL</p>';
        }}
    </script>
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
        """Generate Dockerfile for cross-site scripting vulnerabilities"""

        return '''FROM php:8.0-apache

RUN apt-get update && apt-get install -y \\
    iputils-ping \\
    whois \\
    dnsutils \\
    && rm -rf /var/lib/apt/lists/*

EXPOSE 80

CMD ["apache2-foreground"]
'''
