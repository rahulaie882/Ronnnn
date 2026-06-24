<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

$host = "containers-us-west-11.railway.app";
$db   = "railway";
$user = "root";
$pass = "aowNlPfvoylccbhWKQwnMfPCSMJRWxK";
$port = "3306";

try {
    $dsn = "mysql:host=$host;port=$port;dbname=$db;charset=utf8mb4";
    $conn = new PDO($dsn, $user, $pass);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    echo "<h1>Dashboard Connected Successfully!</h1>";
} catch(PDOException $e) {
    die("Connection failed: " . $e->getMessage());
}
?>
