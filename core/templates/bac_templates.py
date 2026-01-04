"""
Broken Access Control Templates
Generates vulnerable applications for access control issues
"""

import os
import sys
import json

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from templates.base_template import BaseTemplate


class BrokenAccessControlTemplate(BaseTemplate):
    """
    Template generator for Broken Access Control vulnerabilities
    """
    
    def generate_code(self) -> str:
        """Generate vulnerable application based on variant"""
        
        variant = self.config.variant
        
        if "IDOR" in variant:
            return self._generate_idor()
        elif "Horizontal" in variant:
            return self._generate_horizontal_escalation()
        elif "Vertical" in variant:
            return self._generate_vertical_escalation()
        elif "Missing Function" in variant:
            return self._generate_missing_function_access()
        elif "Path Traversal" in variant:
            return self._generate_path_traversal()
        else:
            return self._generate_idor()
    
    def _generate_idor(self) -> str:
        """Generate IDOR vulnerable application"""
        
        app = self.config.application
        constraints = self.config.constraints
        behavior = self.config.behavior
        
        context = app['context']
        param_name = app['param_name']
        resource_type = app['resource_type']
        access_check = constraints['access_check']
        target_id = constraints['target_id']
        current_id = constraints['current_id']
        
        users = behavior['users']
        target_user = behavior['target_user']
        current_user = behavior['current_user']
        
        # Generate users JSON - create as PHP array string
        users_php = "[\n"
        for i, user in enumerate(users):
            users_php += "            [\n"
            users_php += f"                'id' => {user['id']},\n"
            users_php += f"                'username' => '{user['username']}',\n"
            users_php += f"                'email' => '{user['email']}',\n"
            users_php += f"                'role' => '{user['role']}',\n"
            users_php += f"                'created' => '{user['created']}'\n"
            users_php += "            ]"
            if i < len(users) - 1:
                users_php += ","
            users_php += "\n"
        users_php += "        ]"
        
        php_code = f'''<?php
/**
 * Hackforge Machine: {self.machine_id}
 * Vulnerability: IDOR (Insecure Direct Object Reference)
 * Context: {context}
 * Difficulty: {self.difficulty}/5
 */

session_start();

// Fake user database
$users = {users_php};

// Current logged-in user (simulated)
if (!isset($_SESSION['user_id'])) {{
    $_SESSION['user_id'] = {current_user['id']};
    $_SESSION['username'] = '{current_user['username']}';
    $_SESSION['role'] = '{current_user['role']}';
}}

$current_user_id = $_SESSION['user_id'];
$current_username = $_SESSION['username'];
$current_role = $_SESSION['role'];

?>
<!DOCTYPE html>
<html>
<head>
    <title>{context.upper().replace('_', ' ')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1000px;
            margin: 30px auto;
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #eee;
        }}
        h1 {{
            color: #667eea;
            font-size: 2em;
        }}
        .user-info {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 0.9em;
        }}
        .user-info strong {{ color: #fff; }}
        .profile-view {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 10px;
            margin: 20px 0;
        }}
        .profile-view h2 {{
            color: #667eea;
            margin-bottom: 20px;
        }}
        .profile-field {{
            padding: 15px;
            background: white;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid #667eea;
        }}
        .profile-field label {{
            font-weight: bold;
            color: #666;
            display: block;
            margin-bottom: 5px;
        }}
        .profile-field .value {{
            color: #333;
            font-size: 1.1em;
        }}
        .user-list {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .user-card {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            border: 2px solid #eee;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            color: #333;
            display: block;
        }}
        .user-card:hover {{
            border-color: #667eea;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
        }}
        .user-card.current {{
            border-color: #667eea;
            background: #f0f4ff;
        }}
        .user-card .name {{
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}
        .user-card .role {{
            font-size: 0.85em;
            color: #666;
            text-transform: uppercase;
        }}
        .warning {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .secret {{
            background: #d4edda;
            border-left: 4px solid #28a745;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
            font-family: monospace;
            word-break: break-all;
        }}
        .hint {{
            background: #e7f3ff;
            border-left: 4px solid #2196F3;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔐 {context.upper().replace('_', ' ')}</h1>
            <div class="user-info">
                <strong>Logged in as:</strong> {{$current_username}}<br>
                <strong>Role:</strong> {{$current_role}}<br>
                <strong>ID:</strong> {{$current_user_id}}
            </div>
        </div>
        
        <div class="hint">
            💡 <strong>Hint:</strong> Access control checks are {access_check}. Try viewing other users' profiles!
        </div>
        
        <h3 style="margin-top: 30px;">All Users:</h3>
        <div class="user-list">
            <?php foreach ($users as $user): ?>
                <a href="?{param_name}=<?php echo $user['id']; ?>" 
                   class="user-card <?php echo $user['id'] == $current_user_id ? 'current' : ''; ?>">
                    <div class="name"><?php echo htmlspecialchars($user['username']); ?></div>
                    <div class="role"><?php echo htmlspecialchars($user['role']); ?></div>
                </a>
            <?php endforeach; ?>
        </div>
        
        <?php
        if (isset($_GET['{param_name}'])) {{
            $requested_id = $_GET['{param_name}'];
            
            // Find the requested user
            $requested_user = null;
            foreach ($users as $user) {{
                if ($user['id'] == $requested_id) {{
                    $requested_user = $user;
                    break;
                }}
            }}
            
            if ($requested_user) {{
                echo '<div class="profile-view">';
                echo '<h2>Profile: ' . htmlspecialchars($requested_user['username']) . '</h2>';
                
                echo '<div class="profile-field">';
                echo '<label>User ID:</label>';
                echo '<div class="value">' . htmlspecialchars($requested_user['id']) . '</div>';
                echo '</div>';
                
                echo '<div class="profile-field">';
                echo '<label>Username:</label>';
                echo '<div class="value">' . htmlspecialchars($requested_user['username']) . '</div>';
                echo '</div>';
                
                echo '<div class="profile-field">';
                echo '<label>Email:</label>';
                echo '<div class="value">' . htmlspecialchars($requested_user['email']) . '</div>';
                echo '</div>';
                
                echo '<div class="profile-field">';
                echo '<label>Role:</label>';
                echo '<div class="value">' . htmlspecialchars($requested_user['role']) . '</div>';
                echo '</div>';
                
                // Check if this is the target user with the flag
                if ($requested_user['id'] == {target_user['id']}) {{
                    echo '<div class="secret">';
                    echo '<strong>🚩 SECRET DATA (Admin Only):</strong><br><br>';
                    echo '<code>{self.config.flag["content"]}</code>';
                    echo '</div>';
                }}
                
                echo '</div>';
            }} else {{
                echo '<div class="warning">User not found.</div>';
            }}
        }}
        ?>
        
        <div style="margin-top: 40px; color: #666; font-size: 0.85em; text-align: center;">
            Machine ID: {self.machine_id} | Difficulty: {self.difficulty}/5
        </div>
    </div>
</body>
</html>'''
        
        return php_code
    
    def _generate_horizontal_escalation(self) -> str:
        """Generate horizontal privilege escalation"""
        
        behavior = self.config.behavior
        users = behavior['users']
        victim_user = behavior['victim_user']
        attacker_user = behavior['attacker_user']
        
        # Similar to IDOR but with session-based access
        return self._generate_idor()  # Reuse IDOR template with slight modifications
    
    def _generate_vertical_escalation(self) -> str:
        """Generate vertical privilege escalation"""
        
        behavior = self.config.behavior
        users = behavior['users']
        admin_user = behavior['admin_user']
        regular_user = behavior['regular_user']
        constraints = self.config.constraints
        mechanism = constraints['mechanism']
        
        php_code = f'''<?php
/**
 * Hackforge Machine: {self.machine_id}
 * Vulnerability: Vertical Privilege Escalation
 * Mechanism: {mechanism}
 */

session_start();

// Simulate login as regular user
if (!isset($_SESSION['user_id'])) {{
    $_SESSION['user_id'] = {regular_user['id']};
    $_SESSION['username'] = '{regular_user['username']}';
    $_SESSION['role'] = '{regular_user['role']}';
}}

// Check admin access (vulnerable)
function isAdmin() {{
    // Vulnerable check - can be bypassed
    if (isset($_GET['role']) && $_GET['role'] == 'admin') {{
        return true;
    }}
    return $_SESSION['role'] == 'admin';
}}

?>
<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel</title>
    <style>
        body {{ font-family: monospace; background: #1a1a1a; color: #eee; padding: 50px; }}
        .container {{ max-width: 800px; margin: 0 auto; background: #2a2a2a; padding: 40px; border-radius: 10px; }}
        h1 {{ color: #00ff88; }}
        .user-info {{ background: #3a3a3a; padding: 15px; margin: 20px 0; border-radius: 5px; }}
        .admin-panel {{ background: #004400; padding: 20px; margin: 20px 0; border-radius: 5px; }}
        .denied {{ background: #440000; padding: 20px; margin: 20px 0; border-radius: 5px; }}
        .hint {{ color: #888; font-size: 0.9em; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 Admin Control Panel</h1>
        
        <div class="user-info">
            <strong>Current User:</strong> <?php echo $_SESSION['username']; ?><br>
            <strong>Role:</strong> <?php echo $_SESSION['role']; ?><br>
            <strong>User ID:</strong> <?php echo $_SESSION['user_id']; ?>
        </div>
        
        <?php if (isAdmin()): ?>
            <div class="admin-panel">
                <h2>✅ Admin Access Granted</h2>
                <p><strong>Welcome to the admin panel!</strong></p>
                <br>
                <p>🚩 FLAG: <code>{self.config.flag["content"]}</code></p>
            </div>
        <?php else: ?>
            <div class="denied">
                <h2>❌ Access Denied</h2>
                <p>You don't have administrator privileges.</p>
            </div>
        <?php endif; ?>
        
        <div class="hint">
            💡 Hint: The vulnerability mechanism is: {mechanism}<br>
            Try manipulating the role parameter in the URL or session...
        </div>
        
        <div style="margin-top: 40px; color: #666; font-size: 0.85em;">
            Machine ID: {self.machine_id} | Difficulty: {self.difficulty}/5
        </div>
    </div>
</body>
</html>'''
        
        return php_code
    
    def _generate_missing_function_access(self) -> str:
        """Generate missing function-level access control"""
        
        constraints = self.config.constraints
        admin_functions = constraints['protected_functions']
        target_function = constraints['target_function']
        
        # Generate API endpoints
        endpoints_html = ""
        for func in admin_functions:
            endpoints_html += f'<li><code>{func["endpoint"]}</code> - {func["name"]}</li>'
        
        php_code = f'''<?php
/**
 * Hackforge Machine: {self.machine_id}
 * Vulnerability: Missing Function Level Access Control
 */

session_start();

// Simulate regular user login
if (!isset($_SESSION['user_id'])) {{
    $_SESSION['user_id'] = 1;
    $_SESSION['username'] = 'regular_user';
    $_SESSION['role'] = 'user';
}}

// API endpoint handling (no authorization checks!)
if (isset($_GET['action'])) {{
    $action = $_GET['action'];
    
    // These admin functions should check authorization but don't!
    if ($action == 'admin_export') {{
        echo json_encode([
            'status' => 'success',
            'data' => 'Exported data',
            'flag' => '{self.config.flag["content"]}'
        ]);
        exit;
    }}
}}

?>
<!DOCTYPE html>
<html>
<head>
    <title>API Dashboard</title>
    <style>
        body {{ font-family: monospace; background: #f0f0f0; padding: 50px; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 40px; }}
        h1 {{ color: #333; }}
        .endpoint {{ background: #f8f8f8; padding: 15px; margin: 10px 0; border-left: 4px solid #007bff; }}
        code {{ background: #e9ecef; padding: 5px 10px; border-radius: 3px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📡 API Dashboard</h1>
        
        <p><strong>Logged in as:</strong> <?php echo $_SESSION['username']; ?> (<?php echo $_SESSION['role']; ?>)</p>
        
        <h3>Available API Endpoints:</h3>
        <ul>
            {endpoints_html}
        </ul>
        
        <div class="endpoint">
            <p>💡 Hint: Some admin endpoints might not have proper authorization checks!</p>
            <p>Try: <code>?action=admin_export</code></p>
        </div>
        
        <p style="margin-top: 40px; color: #666; font-size: 0.85em;">
            Machine ID: {self.machine_id}
        </p>
    </div>
</body>
</html>'''
        
        return php_code
    
    def _generate_path_traversal(self) -> str:
        """Generate path traversal vulnerability"""
        
        app = self.config.application
        constraints = self.config.constraints
        flag_location = self.config.flag['location']
        
        filters = constraints.get('filters', [])
        
        filter_code = ""
        if 'simple_check' in filters:
            filter_code = "$file = str_replace('../', '', $file);"
        
        php_code = f'''<?php
/**
 * Hackforge Machine: {self.machine_id}
 * Vulnerability: Path Traversal
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>File Viewer</title>
    <style>
        body {{ font-family: monospace; background: #1a1a2e; color: #eee; padding: 50px; }}
        .container {{ max-width: 900px; margin: 0 auto; background: #16213e; padding: 40px; border-radius: 10px; }}
        h1 {{ color: #00ff88; }}
        input {{ width: 70%; padding: 10px; font-size: 1em; }}
        button {{ padding: 10px 20px; font-size: 1em; cursor: pointer; }}
        .content {{ background: #0f3460; padding: 20px; margin-top: 20px; border-radius: 5px; white-space: pre-wrap; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📁 File Viewer</h1>
        
        <form method="GET">
            <input type="text" name="file" placeholder="Enter filename (e.g., document.txt)" 
                   value="<?php echo htmlspecialchars($_GET['file'] ?? ''); ?>">
            <button type="submit">View File</button>
        </form>
        
        <?php
        if (isset($_GET['file'])) {{
            $file = $_GET['file'];
            
            // Weak filter (bypassable)
            {filter_code if filter_code else '// No filters'}
            
            $base_path = '/var/www/html/uploads/';
            $full_path = $base_path . $file;
            
            if (file_exists($full_path)) {{
                $content = file_get_contents($full_path);
                echo '<div class="content">' . htmlspecialchars($content) . '</div>';
            }} else {{
                echo '<div class="content">File not found or access denied.</div>';
            }}
        }}
        ?>
        
        <p style="margin-top: 30px; color: #888;">
            💡 Hint: Flag location is <code>{flag_location}</code><br>
            Try path traversal sequences like ../ or ..\\
        </p>
    </div>
</body>
</html>'''
        
        return php_code
    
    def generate_dockerfile(self) -> str:
        """Generate Dockerfile for BAC vulnerabilities"""
        
        return '''FROM php:8.0-apache

# Enable Apache modules
RUN a2enmod rewrite

# Create upload directory
RUN mkdir -p /var/www/html/uploads && chown www-data:www-data /var/www/html/uploads

# Set permissions
RUN chown -R www-data:www-data /var/www/html

EXPOSE 80

CMD ["apache2-foreground"]
'''
