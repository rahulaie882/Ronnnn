<?p<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);
hp
// Railway dashboard se dekh kar yahan sahi values bhar do
$host = "containers-us-west-11.railway.app"; // Tumhare dashboard mein jo MYSQLHOST hai
$db   = "railway";
$user = "root";
$pass = "aowNlPfvoylccbhWKQwnMfPCSMJRWxK";
$port = "3306"; // Dashboard mein yahi dikh raha hai

try {
    $dsn = "mysql:host=$host;port=$port;dbname=$db;charset=utf8mb4";
    $conn = new PDO($dsn, $user, $pass);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    echo "Connected successfully!"; // Test karne ke liye
} catch(PDOException $e) {
    die("Connection failed: " . $e->getMessage());
}
?>
