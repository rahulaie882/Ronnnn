<?php
// Railway ke environment variables use karo
$host = getenv('MYSQLHOST');
$db   = getenv('MYSQLDATABASE');
$user = getenv('MYSQLUSER');
$pass = getenv('MYSQLPASSWORD');
$port = getenv('MYSQLPORT');

try {
    // Connection string
    $dsn = "mysql:host=$host;port=$port;dbname=$db;charset=utf8mb4";
    $conn = new PDO($dsn, $user, $pass);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    die("Connection failed: " . $e->getMessage());
}

// Data fetch karne ka example (agar use karna ho):
// $stmt = $conn->query("SELECT * FROM setting");
// $settings = $stmt->fetchAll(PDO::FETCH_KEY_PAIR);
?>
