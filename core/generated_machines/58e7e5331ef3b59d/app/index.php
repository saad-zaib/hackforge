<?php
if (isset($_GET['input'])) {
    $input = $_GET['input'];
    echo '<div class="output"><pre>' . htmlspecialchars($input) . '</pre></div>';
}
?>
<!DOCTYPE html>
<html>
<head><title>Command Injection with Filters</title></head>
<body>
    <h1>Command Injection with Filters</h1>
    <form method="GET">
        <input name="input" placeholder="Enter input">
        <button>Submit</button>
    </form>
</body>
</html>