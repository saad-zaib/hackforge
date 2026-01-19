<?php
/**
 * Hackforge Machine: 5c82b9804f4cb764
 * Vulnerability: Error-based SQLi
 * Theme: Matrix Code
 * Difficulty: 1/5
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>Error-based SQLi Challenge</title>
    
    <style>

body {
    font-family: 'Courier New', monospace;
    background: #000;
    color: #0f0;
    margin: 0;
    padding: 0;
    overflow-x: hidden;
    min-height: 100vh;
}

.container {
    max-width: 800px;
    margin: 50px auto;
    padding: 30px;
    background: rgba(0, 20, 0, 0.8);
    border: 2px solid #0f0;
    position: relative;
    animation: glitch 3s infinite;
}

@keyframes glitch {
    0%, 100% { transform: translate(0); }
    20% { transform: translate(-2px, 2px); }
    40% { transform: translate(2px, -2px); }
    60% { transform: translate(-2px, -2px); }
    80% { transform: translate(2px, 2px); }
}

h1 {
    color: #0f0;
    text-shadow: 0 0 5px #0f0;
    animation: flicker 1.5s infinite alternate;
    text-transform: uppercase;
    letter-spacing: 5px;
    margin-top: 0;
}

@keyframes flicker {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.8; }
}

p {
    color: #0d0;
}

input {
    background: #001100;
    border: 1px solid #0f0;
    color: #0f0;
    padding: 12px;
    width: 100%;
    box-sizing: border-box;
    font-family: 'Courier New', monospace;
    font-size: 14px;
}

input:focus {
    outline: none;
    box-shadow: 0 0 10px #0f0;
}

button {
    background: transparent;
    border: 2px solid #0f0;
    color: #0f0;
    padding: 12px 30px;
    cursor: pointer;
    font-family: 'Courier New', monospace;
    text-transform: uppercase;
    margin-top: 10px;
    transition: all 0.3s;
}

button:hover {
    background: #0f0;
    color: #000;
    box-shadow: 0 0 15px #0f0;
}

.result {
    margin-top: 30px;
    border: 1px solid #0f0;
    padding: 15px;
    background: rgba(0, 255, 0, 0.05);
}

.hint {
    margin-top: 20px;
    padding: 15px;
    border: 1px dashed #0f0;
    background: rgba(0, 255, 0, 0.03);
}

    </style>
</head>
<body>
    <div class="container">
        <h1>Error-based SQLi</h1>
        <p>Context: search_functionality</p>

        <form method="GET">
            <input type="text" name="input" placeholder="_ ">
            <button type="submit">[ EXECUTE QUERY ]</button>
        </form>

        <?php
        if (isset($_GET['input'])) {
            $input = $_GET['input'];
            // No filters
            echo '<div class="result">';
            echo '<h3>Results:</h3>';
            echo '<div>' . $input . '</div>';
            echo '</div>';
        }
        ?>

        <div class="hint">
            <strong>💡 Hint:</strong> This is a search_functionality context. Can you find the vulnerability?
        </div>
    </div>
</body>
</html>