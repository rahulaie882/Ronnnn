<?php
// Database connection
$host = "containers-us-west-11.railway.app";
$db   = "railway";
$user = "root";
$pass = "aowNlPfvoylccbhWKQwnMfPCSMJRWxK";
$port = "3306";

$conn = new mysqli($host, $user, $pass, $db, $port);

if ($conn->connect_error) {
    echo "Connection Error: " . $conn->connect_error;
} else {
    echo "<h1>Connected Successfully!</h1>";
}
?>
