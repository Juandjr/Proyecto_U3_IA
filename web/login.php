<?php
session_start();
include "conexion.php";
$email = $_POST['email'];
$password = $_POST['password'];
$sql = "SELECT * FROM usuarios WHERE email = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $email);
$stmt->execute();
$result = $stmt->get_result();
if ($result->num_rows === 1) {
    $user = $result->fetch_assoc();
    if (password_verify($password, $user['password'])) {
        $_SESSION['id_usuario'] = $user['id_usuario'];
        $_SESSION['telefono']   = $user['telefono'];
        $conn->query("UPDATE usuarios SET activo = 0");
        $stmt2 = $conn->prepare(
            "UPDATE usuarios SET activo = 1 WHERE id_usuario = ?"
        );
        $stmt2->bind_param("i", $user['id_usuario']);
        $stmt2->execute();
        header("Location: index.php");
        exit();
    } else {
        $msg = "Contraseña incorrecta";
        header("Location: login.html?error=" . urlencode($msg));
        exit;
    }
} else {
    $msg = "Usuario no encontrado";
    header("Location: login.html?error=" . urlencode($msg));
    exit;
}
