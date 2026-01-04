<?php
/**
 * Hackforge Machine: be49b5e0cc3bf8d8
 * Vulnerability: Vertical Privilege Escalation
 * Mechanism: jwt_role_manipulation
 */

session_start();

// Simulate login as regular user
if (!isset($_SESSION['user_id'])) {
    $_SESSION['user_id'] = 1;
    $_SESSION['username'] = 'user1';
    $_SESSION['role'] = 'user';
}

// Check admin access (vulnerable)
function isAdmin() {
    // Vulnerable check - can be bypassed
    if (isset($_GET['role']) && $_GET['role'] == 'admin') {
        return true;
    }
    return $_SESSION['role'] == 'admin';
}

?>
<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel</title>
    <style>
        body { font-family: monospace; background: #1a1a1a; color: #eee; padding: 50px; }
        .container { max-width: 800px; margin: 0 auto; background: #2a2a2a; padding: 40px; border-radius: 10px; }
        h1 { color: #00ff88; }
        .user-info { background: #3a3a3a; padding: 15px; margin: 20px 0; border-radius: 5px; }
        .admin-panel { background: #004400; padding: 20px; margin: 20px 0; border-radius: 5px; }
        .denied { background: #440000; padding: 20px; margin: 20px 0; border-radius: 5px; }
        .hint { color: #888; font-size: 0.9em; margin-top: 20px; }
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
                <p>🚩 FLAG: <code>HACKFORGE{07c3c58e9150efd0e484084bd27d9a99}</code></p>
            </div>
        <?php else: ?>
            <div class="denied">
                <h2>❌ Access Denied</h2>
                <p>You don't have administrator privileges.</p>
            </div>
        <?php endif; ?>
        
        <div class="hint">
            💡 Hint: The vulnerability mechanism is: jwt_role_manipulation<br>
            Try manipulating the role parameter in the URL or session...
        </div>
        
        <div style="margin-top: 40px; color: #666; font-size: 0.85em;">
            Machine ID: be49b5e0cc3bf8d8 | Difficulty: 3/5
        </div>
    </div>
</body>
</html>