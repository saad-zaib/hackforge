<?php
/**
 * Hackforge Machine: 67b4e02428bd76dc
 * Vulnerability: NoSQL Injection
 * Database: MongoDB
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>NoSQL User Search</title>
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
        }
        h1 {
            color: #00ff88;
            font-size: 2.5em;
            margin-bottom: 30px;
        }
        input[type="text"] {
            width: 100%;
            padding: 15px;
            background: rgba(0, 0, 0, 0.4);
            border: 2px solid #00ff88;
            border-radius: 8px;
            color: #fff;
            font-size: 1em;
            margin: 15px 0;
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
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 User Search</h1>

        <form method="GET">
            <input type="text"
                   name="category"
                   placeholder="Enter username"
                   value="<?php echo htmlspecialchars($_GET['category'] ?? ''); ?>"
                   autofocus>
            <button type="submit">Search</button>
        </form>

        <?php
        if (isset($_GET['category'])) {
            echo '<div class="output">';
            echo "<strong>Search Results:</strong>\n\n";

            $input = $_GET['category'];

            try {
                // Connect to MongoDB
                $manager = new MongoDB\Driver\Manager("mongodb://localhost:27017");

                // Vulnerable query - accepts array input for NoSQL injection
                $filter = ['category' => $input];
                $query = new MongoDB\Driver\Query($filter);

                $cursor = $manager->executeQuery("hackforge.users", $query);

                foreach ($cursor as $document) {
                    echo "Username: " . htmlspecialchars($document->username) . "\n";
                    echo "Email: " . htmlspecialchars($document->email) . "\n";
                    echo "---\n";
                }
            } catch (Exception $e) {
                echo "Error: " . htmlspecialchars($e->getMessage());
            }

            echo '</div>';
        }
        ?>
    </div>
</body>
</html>