<?php
/**
 * Machine: 8ed8fa14892a2b42
 * Variant: Error-based SQL Injection
 * Difficulty: 2/5
 * Context: login_form
 */

// Database connection
$conn = mysqli_connect('db', 'hackforge', 'hackforge123', 'hackforge');
if (!$conn) {
    die('<div class="error">Connection failed: ' . mysqli_connect_error() . '</div>');
}

// Process user input if provided
if (isset($_GET['input'])) {
    $input = $_GET['input'];
    
    $input = $_GET['input'];
    // Apply filters
    $input = str_replace("'", "", $input);
    $input = str_replace("OR", "", $input);

    // Vulnerable operation
    $query = "SELECT * FROM users WHERE username='" . $input . "' AND password='password'";
    $result = mysqli_query($conn, $query);

    if ($result) {
        echo "Query executed successfully.";
    } else {
        echo mysqli_error($conn);
    }
}

// Close database connection
mysqli_close($conn);
?>
<!DOCTYPE html>
<html>
<head>
    <title>Error-based SQL Injection</title>
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            max-width: 900px;
            margin: 50px auto;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #fff;
            padding: 20px;
        }
        .container {
            background: rgba(42, 42, 42, 0.95);
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
            border: 1px solid rgba(231, 76, 60, 0.3);
        }
        h1 {
            color: #e74c3c;
            margin-bottom: 10px;
            font-size: 2em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .info {
            background: rgba(52, 73, 94, 0.5);
            padding: 15px;
            border-radius: 6px;
            margin: 20px 0;
            border-left: 4px solid #3498db;
        }
        .info strong { color: #3498db; }
        input, button {
            padding: 14px;
            margin: 10px 0;
            font-size: 16px;
            width: 100%;
            box-sizing: border-box;
            border-radius: 6px;
        }
        input {
            background: #2c3e50;
            border: 2px solid #34495e;
            color: #ecf0f1;
            transition: border-color 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #e74c3c;
        }
        button {
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
            color: white;
            border: none;
            cursor: pointer;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(231, 76, 60, 0.4);
        }
        .result, .error, .output {
            margin-top: 20px;
            padding: 20px;
            background: rgba(44, 62, 80, 0.5);
            border-left: 4px solid #e74c3c;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
        }
        .error {
            border-left-color: #e67e22;
            background: rgba(230, 126, 34, 0.1);
        }
        .output {
            border-left-color: #27ae60;
            background: rgba(39, 174, 96, 0.1);
        }
        pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            margin: 0;
            color: #ecf0f1;
        }
        .hint {
            margin-top: 20px;
            padding: 20px;
            background: rgba(26, 71, 42, 0.5);
            border-left: 4px solid #27ae60;
            border-radius: 6px;
            font-size: 14px;
        }
        .hint strong { color: #2ecc71; }
        code {
            background: rgba(52, 152, 219, 0.2);
            padding: 2px 6px;
            border-radius: 3px;
            color: #3498db;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Error-based SQL Injection</h1>

        <div class="info">
            <p><strong>Context:</strong> User authentication system</p>
            <p><strong>Difficulty:</strong> 2/5</p>
            <p><strong>Machine ID:</strong> <code>8ed8fa14892a2b42</code></p>
        </div>

        <form method="GET">
            <input
                name="input"
                placeholder="Enter your payload here..."
                value="<?php echo isset($_GET['input']) ? htmlspecialchars($_GET['input']) : ''; ?>"
                autofocus
            >
            <button type="submit">🚀 Execute</button>
        </form>

        <div class="hint">
            <strong>💡 Challenge Hint:</strong> Try to exploit the error-based sql injection in the login_form context.
        </div>
    </div>
</body>
</html>