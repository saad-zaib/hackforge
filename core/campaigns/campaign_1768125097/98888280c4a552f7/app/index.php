<?php
/**
 * Hackforge Machine: {self.machine_id}
 * Vulnerability: Reflected XSS
 * Theme: {self.theme['name']}
 * Difficulty: {self.difficulty}/5
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>Reflected XSS Challenge</title>
    {fonts_import}
    <style>
{theme_css}
    </style>
</head>
<body>
    <div class="container">
        <h1>Reflected XSS</h1>
        <p>Context: {context}</p>

        <form method="GET">
            <input type="text" name="input" placeholder="{placeholder}">
            <button type="submit">{button_text}</button>
        </form>

        <?php
        if (isset($_GET['input'])) {
            $input = $_GET['input'];
            {filter_code if filter_code else '// No filters'}
            echo '<div class="result">';
            echo '<h3>Results:</h3>';
            echo '<div>' . $input . '</div>';
            echo '</div>';
        }
        ?>

        <div class="hint">
            <strong>💡 Hint:</strong> This is a {context} context. Can you find the vulnerability?
        </div>
    </div>
</body>
</html>