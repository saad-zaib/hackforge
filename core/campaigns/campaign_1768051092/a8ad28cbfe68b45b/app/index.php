<?php
/**
 * Hackforge Machine: a8ad28cbfe68b45b
 * Vulnerability: Reflected XSS
 * Context: search_box
 * Difficulty: 2/5
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>Reflected XSS Challenge</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
            padding: 20px;
            margin: 0;
        }
        .container {
            max-width: 900px;
            margin: 50px auto;
            background: rgba(15, 32, 39, 0.9);
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(0, 255, 136, 0.1);
        }
        h1 {
            color: #00ff88;
            text-align: center;
            margin-bottom: 30px;
        }
        input {
            width: 100%;
            padding: 15px;
            background: rgba(0, 0, 0, 0.4);
            border: 2px solid #00ff88;
            color: #fff;
            font-size: 16px;
            border-radius: 5px;
            margin-bottom: 15px;
            box-sizing: border-box;
        }
        button {
            background: #00ff88;
            color: #000;
            padding: 15px 40px;
            border: none;
            cursor: pointer;
            font-weight: bold;
            border-radius: 5px;
            width: 100%;
        }
        button:hover {
            background: #00cc6a;
        }
        .result {
            margin-top: 30px;
            padding: 20px;
            background: rgba(0, 0, 0, 0.3);
            border-left: 4px solid #00ff88;
            border-radius: 5px;
        }
        .hint {
            margin-top: 20px;
            padding: 15px;
            background: rgba(255, 193, 7, 0.1);
            border-left: 4px solid #ffc107;
            border-radius: 5px;
            font-size: 14px;
        }
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
        if (isset($_GET['input'])) {
            $input = $_GET['input'];
            
            $input = str_replace('s', '', $input);
            $input = str_replace('o', '', $input);
            
            echo '<div class="result">';
            echo '<h3>Search Results for: ' . $input . '</h3>';
            echo '<p>Showing results for your query...</p>';
            echo '</div>';
        }
        ?>
        
        <div class="hint">
            <strong>💡 Hint:</strong> This is a search_box context. Can you find the vulnerability?
        </div>
    </div>
</body>
</html>