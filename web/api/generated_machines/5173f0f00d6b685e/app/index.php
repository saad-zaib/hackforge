<?php
/**
 * Hackforge Machine: 5173f0f00d6b685e
 * Vulnerability: SQL Injection
 * Context: file_processor
 * Database: mariadb
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>FILE PROCESSOR</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #2c1e4e 0%, #1a1a3e 100%);
            color: #eee;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 50px auto;
            background: rgba(20, 20, 40, 0.9);
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(138, 43, 226, 0.3);
            border: 1px solid rgba(138, 43, 226, 0.4);
        }
        h1 {
            color: #9370db;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 0 0 10px rgba(147, 112, 219, 0.5);
        }
        .info-box {
            background: rgba(138, 43, 226, 0.1);
            border-left: 4px solid #9370db;
            padding: 15px;
            margin-bottom: 25px;
            border-radius: 5px;
        }
        .info-box strong { color: #9370db; }
        input[type="text"] {
            width: 100%;
            padding: 15px;
            background: rgba(0, 0, 0, 0.4);
            border: 2px solid #9370db;
            border-radius: 8px;
            color: #fff;
            font-size: 1em;
            font-family: 'Courier New', monospace;
            margin: 15px 0;
        }
        button {
            background: linear-gradient(135deg, #9370db 0%, #7b68ee 100%);
            color: #fff;
            border: none;
            padding: 15px 40px;
            font-size: 1.1em;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(147, 112, 219, 0.4);
        }
        .output {
            background: rgba(0, 0, 0, 0.6);
            border: 2px solid #9370db;
            border-radius: 8px;
            padding: 20px;
            margin-top: 25px;
            min-height: 150px;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            color: #dda0dd;
        }
        .filters {
            background: rgba(255, 0, 0, 0.1);
            border-left: 4px solid #ff4444;
            padding: 10px;
            margin: 15px 0;
            border-radius: 5px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🗄️ FILE PROCESSOR</h1>
        
        <div class="info-box">
            <strong>Machine ID:</strong> <code>5173f0f00d6b685e</code><br>
            <strong>Database:</strong> mariadb<br>
            <strong>Parameter:</strong> <code>id</code>
        </div>
        
        <div class="filters">⚠️ Security Filters Active: space, semicolon</div>
        
        <form method="GET">
            <input type="text" 
                   name="id" 
                   placeholder="Enter id"
                   value="<?php echo htmlspecialchars($_GET['id'] ?? ''); ?>"
                   autofocus>
            <button type="submit">🔍 Search</button>
        </form>
        
        <?php
        if (isset($_GET['id'])) {
            echo '<div class="output">';
            echo "<strong>Query Results:</strong>\n\n";
            
            $input = $_GET['id'];
            
            // Security filters
            $input = str_replace(' ', '', $input);
            $input = str_replace(';', '', $input);
            
            // Database query
            
    $db = new SQLite3('/tmp/hackforge.db');
            
    $query = "SELECT * FROM items WHERE id=" . $input . "";
    $result = $db->query($query);
    
    if ($result) {
        while($row = $result->fetchArray(SQLITE3_ASSOC)) {
            foreach($row as $key => $value) {
                echo htmlspecialchars($key) . ": " . htmlspecialchars($value) . "\n";
            }
            echo "---\n";
        }
    } else {
        echo "Error: " . $db->lastErrorMsg();
    }
            
            echo '</div>';
        }
        ?>
    </div>
</body>
</html>