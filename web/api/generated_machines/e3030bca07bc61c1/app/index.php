<?php
/**
 * Hackforge Machine: e3030bca07bc61c1
 * Vulnerability: Command Injection
 * Context: login_form
 * Difficulty: 2/5
 * 
 * EDUCATIONAL PURPOSE ONLY
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>LOGIN FORM Tool</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 50px auto;
            background: rgba(15, 32, 39, 0.9);
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 255, 136, 0.2);
            border: 1px solid rgba(0, 255, 136, 0.3);
        }
        h1 {
            color: #00ff88;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
        }
        .subtitle {
            color: #888;
            font-size: 0.9em;
            margin-bottom: 30px;
        }
        .info-box {
            background: rgba(0, 255, 136, 0.1);
            border-left: 4px solid #00ff88;
            padding: 15px;
            margin-bottom: 25px;
            border-radius: 5px;
        }
        .info-box strong { color: #00ff88; }
        .form-group {
            margin: 25px 0;
        }
        label {
            display: block;
            color: #00ff88;
            margin-bottom: 10px;
            font-weight: bold;
        }
        input[type="text"] {
            width: 100%;
            padding: 15px;
            background: rgba(0, 0, 0, 0.4);
            border: 2px solid #00ff88;
            border-radius: 8px;
            color: #fff;
            font-size: 1em;
            font-family: 'Courier New', monospace;
            transition: all 0.3s;
        }
        input[type="text"]:focus {
            outline: none;
            border-color: #00ffff;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
        }
        button {
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
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0, 255, 136, 0.4);
        }
        .clear-btn {
            background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%);
            color: #fff;
        }
        .examples {
            background: rgba(0, 255, 136, 0.05);
            border: 1px solid rgba(0, 255, 136, 0.2);
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
        }
        .examples h3 {
            color: #00ff88;
            font-size: 1em;
            margin-bottom: 10px;
        }
        .example-cmd {
            background: rgba(0, 0, 0, 0.4);
            padding: 8px 12px;
            margin: 5px 0;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            cursor: pointer;
            transition: all 0.2s;
            display: inline-block;
            color: #0ff;
        }
        .example-cmd:hover {
            background: rgba(0, 255, 136, 0.2);
            transform: translateX(5px);
        }
        .output {
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
        }
        .hint {
            color: #666;
            font-size: 0.85em;
            margin-top: 20px;
            text-align: center;
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
    <script>
        function fillExample(cmd) {
            document.getElementById('hostname').value = cmd;
        }
        function clearOutput() {
            window.location.href = window.location.pathname;
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>🔧 LOGIN FORM</h1>
        <div class="subtitle">Network Diagnostic Tool</div>
        
        <div class="info-box">
            <strong>Machine ID:</strong> <code>e3030bca07bc61c1</code><br>
            <strong>Difficulty:</strong> 2/5<br>
            <strong>Parameter:</strong> <code>hostname</code>
        </div>
        
        <div class="filters">⚠️ Security Filters Active: space, semicolon</div>
        
        <div class="examples">
            <h3>💡 Try These Examples:</h3>
            <div class="example-cmd" onclick="fillExample('google.com')">📍 google.com</div>
            <div class="example-cmd" onclick="fillExample('8.8.8.8')">📍 8.8.8.8</div>
            <div class="example-cmd" onclick="fillExample('localhost')">📍 localhost</div>
        </div>
        
        <form method="GET">
            <div class="form-group">
                <label for="hostname">Enter hostname:</label>
                <input type="text" 
                       id="hostname" 
                       name="hostname" 
                       placeholder="e.g., google.com, 8.8.8.8"
                       value="<?php echo htmlspecialchars($_GET['hostname'] ?? ''); ?>"
                       autofocus>
            </div>
            <button type="submit">▶ Execute Command</button>
            <button type="button" class="clear-btn" onclick="clearOutput()">🔄 Clear</button>
        </form>
        
        <?php
        if (isset($_GET['hostname'])) {
            echo '<div class="output">';
            echo "<strong>⚡ Executing command...</strong>\n\n";
            
            $input = $_GET['hostname'];
            
            // Security filters (bypassable)
            $input = str_replace(' ', '', $input);
            $input = str_replace(';', '', $input);
            
            // Execute command
            $command = "nslookup " . $input . " 2>&1";
            $output = shell_exec($command);
            
            if ($output) {
                echo htmlspecialchars($output);
            } else {
                echo "No output returned.";
            }
            
            echo '</div>';
        }
        ?>
        
        <div class="hint">
            💡 Can you find the flag? Try exploring the system...
        </div>
    </div>
</body>
</html>