<?php
/**
 * Hackforge Machine: 55ff626ceefcf2c8
 * Vulnerability: Path Traversal
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>File Viewer</title>
    <style>
        body { font-family: monospace; background: #1a1a2e; color: #eee; padding: 50px; }
        .container { max-width: 900px; margin: 0 auto; background: #16213e; padding: 40px; border-radius: 10px; }
        h1 { color: #00ff88; }
        input { width: 70%; padding: 10px; font-size: 1em; }
        button { padding: 10px 20px; font-size: 1em; cursor: pointer; }
        .content { background: #0f3460; padding: 20px; margin-top: 20px; border-radius: 5px; white-space: pre-wrap; }
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
        if (isset($_GET['file'])) {
            $file = $_GET['file'];
            
            // Weak filter (bypassable)
            // No filters
            
            $base_path = '/var/www/html/uploads/';
            $full_path = $base_path . $file;
            
            if (file_exists($full_path)) {
                $content = file_get_contents($full_path);
                echo '<div class="content">' . htmlspecialchars($content) . '</div>';
            } else {
                echo '<div class="content">File not found or access denied.</div>';
            }
        }
        ?>
        
        <p style="margin-top: 30px; color: #888;">
            💡 Hint: Flag location is <code>/var/www/flag.txt</code><br>
            Try path traversal sequences like ../ or ..\
        </p>
    </div>
</body>
</html>