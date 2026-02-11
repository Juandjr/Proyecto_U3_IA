<?php
include "conexion.php";
$nombre = $_POST['nombre'];
$email = $_POST['email'];
$raw_password = $_POST['password'];
$telefono = $_POST['telefono'];
if (!preg_match('/^9\d{8}$/', $telefono)) {
    $msg = "Teléfono inválido. Debe comenzar con 9 y tener 9 dígitos.";
    header("Location: register.html?error=" . urlencode($msg));
    exit;
}
if (!preg_match('/[A-Z]/', $raw_password) || !preg_match('/[^A-Za-z0-9]/', $raw_password)) {
    $msg = "Contraseña inválida. Debe contener al menos una letra mayúscula y un símbolo.";
    header("Location: register.html?error=" . urlencode($msg));
    exit;
}
$password = password_hash($raw_password, PASSWORD_DEFAULT);
$sql = "INSERT INTO usuarios (nombre, email, password, telefono)
        VALUES (?, ?, ?, ?)";
$stmt = $conn->prepare($sql);
$stmt->bind_param("ssss", $nombre, $email, $password, $telefono);
if ($stmt->execute()) {
    header("Location: login.html");
} else {
    $msg = "Error al registrar. Intente nuevamente.";
    header("Location: register.html?error=" . urlencode($msg));
}
