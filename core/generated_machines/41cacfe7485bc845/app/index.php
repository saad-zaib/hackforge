<?php
/**
 * Hackforge Machine: 41cacfe7485bc845
 * Vulnerability: Basic Path Traversal
 * Theme: Sunset Gradient
 * Difficulty: 2/5
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>Basic Path Traversal Challenge</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
    <style>

body {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    background-attachment: fixed;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0;
    padding: 20px;
}

.container {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 25px;
    padding: 50px;
    max-width: 650px;
    width: 100%;
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2);
}

h1 {
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-top: 0;
    font-size: 36px;
    font-weight: 600;
}

p {
    color: #555;
}

input {
    background: #f8f9fa;
    border: 2px solid #e9ecef;
    color: #333;
    padding: 15px;
    border-radius: 12px;
    width: 100%;
    box-sizing: border-box;
    font-size: 16px;
    font-family: 'Poppins', sans-serif;
    transition: all 0.3s;
}

input:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

button {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: #fff;
    border: none;
    padding: 15px 40px;
    border-radius: 12px;
    font-weight: 600;
    cursor: pointer;
    margin-top: 15px;
    font-size: 16px;
    transition: all 0.3s;
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
}

.result {
    margin-top: 30px;
    padding: 20px;
    background: linear-gradient(135deg, #f093fb15, #667eea15);
    border-radius: 12px;
    border-left: 4px solid #667eea;
}

.hint {
    margin-top: 20px;
    padding: 15px;
    background: #fff3cd;
    border-left: 4px solid #feca57;
    border-radius: 8px;
    color: #856404;
}

    </style>
</head>
<body>
    <div class="container">
        <h1>Basic Path Traversal</h1>
        <p>Context: document_portal</p>

        <form method="GET">
            <input type="text" name="input" placeholder="Type your query...">
            <button type="submit">Submit</button>
        </form>

        <?php
        if (isset($_GET['input'])) {
            $input = $_GET['input'];
            $input = str_replace('d', '', $input);
            echo '<div class="result">';
            echo '<h3>Results:</h3>';
            echo '<div>' . $input . '</div>';
            echo '</div>';
        }
        ?>

        <div class="hint">
            <strong>💡 Hint:</strong> This is a document_portal context. Can you find the vulnerability?
        </div>
    </div>
</body>
</html>