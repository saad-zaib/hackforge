<?php
/**
 * Hackforge Machine: 469852811c1c3455
 * Vulnerability: Missing Function Level Access Control
 */

session_start();

// Simulate regular user login
if (!isset($_SESSION['user_id'])) {
    $_SESSION['user_id'] = 1;
    $_SESSION['username'] = 'regular_user';
    $_SESSION['role'] = 'user';
}

// API endpoint handling (no authorization checks!)
if (isset($_GET['action'])) {
    $action = $_GET['action'];
    
    // These admin functions should check authorization but don't!
    if ($action == 'admin_export') {
        echo json_encode([
            'status' => 'success',
            'data' => 'Exported data',
            'flag' => 'HACKFORGE{41be9c0bc14b8eabd5d895915620e0f4}'
        ]);
        exit;
    }
}

?>
<!DOCTYPE html>
<html>
<head>
    <title>API Dashboard</title>
    <style>
        body { font-family: monospace; background: #f0f0f0; padding: 50px; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; }
        h1 { color: #333; }
        .endpoint { background: #f8f8f8; padding: 15px; margin: 10px 0; border-left: 4px solid #007bff; }
        code { background: #e9ecef; padding: 5px 10px; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📡 API Dashboard</h1>
        
        <p><strong>Logged in as:</strong> <?php echo $_SESSION['username']; ?> (<?php echo $_SESSION['role']; ?>)</p>
        
        <h3>Available API Endpoints:</h3>
        <ul>
            <li><code>/api/admin/users/delete</code> - delete_user</li><li><code>/api/admin/data/all</code> - view_all_data</li><li><code>/api/admin/settings</code> - modify_settings</li><li><code>/api/admin/export</code> - export_database</li>
        </ul>
        
        <div class="endpoint">
            <p>💡 Hint: Some admin endpoints might not have proper authorization checks!</p>
            <p>Try: <code>?action=admin_export</code></p>
        </div>
        
        <p style="margin-top: 40px; color: #666; font-size: 0.85em;">
            Machine ID: 469852811c1c3455
        </p>
    </div>
</body>
</html>