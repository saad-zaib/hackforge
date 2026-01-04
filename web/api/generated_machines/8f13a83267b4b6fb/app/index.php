<?php
/**
 * Hackforge Machine: 8f13a83267b4b6fb
 * Vulnerability: IDOR (Insecure Direct Object Reference)
 * Context: e_commerce_order
 * Difficulty: 2/5
 */

session_start();

// Fake user database
$users = [
            [
                'id' => 1,
                'username' => 'user1',
                'email' => 'user1@example.com',
                'role' => 'user',
                'created' => '2025-01-01'
            ],
            [
                'id' => 2,
                'username' => 'user2',
                'email' => 'user2@example.com',
                'role' => 'user',
                'created' => '2025-01-01'
            ],
            [
                'id' => 3,
                'username' => 'user3',
                'email' => 'user3@example.com',
                'role' => 'user',
                'created' => '2025-01-01'
            ],
            [
                'id' => 4,
                'username' => 'user4',
                'email' => 'user4@example.com',
                'role' => 'moderator',
                'created' => '2025-01-01'
            ],
            [
                'id' => 5,
                'username' => 'user5',
                'email' => 'user5@example.com',
                'role' => 'admin',
                'created' => '2025-01-01'
            ],
            [
                'id' => 6,
                'username' => 'user6',
                'email' => 'user6@example.com',
                'role' => 'user',
                'created' => '2025-01-01'
            ],
            [
                'id' => 7,
                'username' => 'user7',
                'email' => 'user7@example.com',
                'role' => 'user',
                'created' => '2025-01-01'
            ],
            [
                'id' => 8,
                'username' => 'user8',
                'email' => 'user8@example.com',
                'role' => 'user',
                'created' => '2025-01-01'
            ],
            [
                'id' => 9,
                'username' => 'user9',
                'email' => 'user9@example.com',
                'role' => 'moderator',
                'created' => '2025-01-01'
            ],
            [
                'id' => 10,
                'username' => 'user10',
                'email' => 'user10@example.com',
                'role' => 'admin',
                'created' => '2025-01-01'
            ]
        ];

// Current logged-in user (simulated)
if (!isset($_SESSION['user_id'])) {
    $_SESSION['user_id'] = 8;
    $_SESSION['username'] = 'user8';
    $_SESSION['role'] = 'user';
}

$current_user_id = $_SESSION['user_id'];
$current_username = $_SESSION['username'];
$current_role = $_SESSION['role'];

?>
<!DOCTYPE html>
<html>
<head>
    <title>E COMMERCE ORDER</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1000px;
            margin: 30px auto;
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #eee;
        }
        h1 {
            color: #667eea;
            font-size: 2em;
        }
        .user-info {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 0.9em;
        }
        .user-info strong { color: #fff; }
        .profile-view {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 10px;
            margin: 20px 0;
        }
        .profile-view h2 {
            color: #667eea;
            margin-bottom: 20px;
        }
        .profile-field {
            padding: 15px;
            background: white;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid #667eea;
        }
        .profile-field label {
            font-weight: bold;
            color: #666;
            display: block;
            margin-bottom: 5px;
        }
        .profile-field .value {
            color: #333;
            font-size: 1.1em;
        }
        .user-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .user-card {
            background: white;
            padding: 15px;
            border-radius: 8px;
            border: 2px solid #eee;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            color: #333;
            display: block;
        }
        .user-card:hover {
            border-color: #667eea;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
        }
        .user-card.current {
            border-color: #667eea;
            background: #f0f4ff;
        }
        .user-card .name {
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }
        .user-card .role {
            font-size: 0.85em;
            color: #666;
            text-transform: uppercase;
        }
        .warning {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }
        .secret {
            background: #d4edda;
            border-left: 4px solid #28a745;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
            font-family: monospace;
            word-break: break-all;
        }
        .hint {
            background: #e7f3ff;
            border-left: 4px solid #2196F3;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔐 E COMMERCE ORDER</h1>
            <div class="user-info">
                <strong>Logged in as:</strong> {$current_username}<br>
                <strong>Role:</strong> {$current_role}<br>
                <strong>ID:</strong> {$current_user_id}
            </div>
        </div>
        
        <div class="hint">
            💡 <strong>Hint:</strong> Access control checks are client_side_only. Try viewing other users' profiles!
        </div>
        
        <h3 style="margin-top: 30px;">All Users:</h3>
        <div class="user-list">
            <?php foreach ($users as $user): ?>
                <a href="?user_id=<?php echo $user['id']; ?>" 
                   class="user-card <?php echo $user['id'] == $current_user_id ? 'current' : ''; ?>">
                    <div class="name"><?php echo htmlspecialchars($user['username']); ?></div>
                    <div class="role"><?php echo htmlspecialchars($user['role']); ?></div>
                </a>
            <?php endforeach; ?>
        </div>
        
        <?php
        if (isset($_GET['user_id'])) {
            $requested_id = $_GET['user_id'];
            
            // Find the requested user
            $requested_user = null;
            foreach ($users as $user) {
                if ($user['id'] == $requested_id) {
                    $requested_user = $user;
                    break;
                }
            }
            
            if ($requested_user) {
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
                if ($requested_user['id'] == 10) {
                    echo '<div class="secret">';
                    echo '<strong>🚩 SECRET DATA (Admin Only):</strong><br><br>';
                    echo '<code>HACKFORGE{917526c11a1969d7beb54e5e45f1b382}</code>';
                    echo '</div>';
                }
                
                echo '</div>';
            } else {
                echo '<div class="warning">User not found.</div>';
            }
        }
        ?>
        
        <div style="margin-top: 40px; color: #666; font-size: 0.85em; text-align: center;">
            Machine ID: 8f13a83267b4b6fb | Difficulty: 2/5
        </div>
    </div>
</body>
</html>