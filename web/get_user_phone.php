<?php
require "conexion.php";

$sql = "SELECT telefono FROM usuarios WHERE activo = 1 LIMIT 1";
$result = $conn->query($sql);

if ($row = $result->fetch_assoc()) {
    echo trim($row['telefono']);
} else {
    echo "";
}
