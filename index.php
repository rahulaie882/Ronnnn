
<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Connection
$conn = new mysqli(getenv('MYSQLHOST'), getenv('MYSQLUSER'), getenv('MYSQLPASSWORD'), getenv('MYSQLDATABASE'), getenv('MYSQLPORT'));

if ($conn->connect_error) { die("Connection Failed"); }

// Update Logic
if (isset($_POST['update_all'])) {
    $conn->query("UPDATE setting SET value='".$_POST['price']."' WHERE key_name='price'");
    $conn->query("UPDATE setting SET value='".$_POST['upi']."' WHERE key_name='upi'");
    echo "<h3>Updated Successfully!</h3>";
}

// Data Fetching
$settings = [];
$res = $conn->query("SELECT * FROM setting");
while($row = $res->fetch_assoc()) { $settings[$row['key_name']] = $row['value']; }
?>

<h2>VIAXOR Dashboard</h2>
<form method="POST">
    Price: <input type="text" name="price" value="<?php echo $settings['price'] ?? ''; ?>"><br>
    UPI: <input type="text" name="upi" value="<?php echo $settings['upi'] ?? ''; ?>"><br>
    <button type="submit" name="update_all">Save</button>
</form>

