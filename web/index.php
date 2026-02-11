<?php
session_start();
if (!isset($_SESSION['id_usuario'])) {
    header("Location: login.html");
    exit();
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>WorkSafe | Detección PPE</title>
    <link rel="stylesheet" href="./assets/css/index.css">
</head>
<body>
<header class="top-bar">
    <div class="brand">
        <img src="./assets/img/logo.png" alt="WorkSafe Logo">
        <h2>Detección PPE</h2>
    </div>

    <a href="logout.php" class="logout-btn">Cerrar sesión</a>
</header>
<main>
    <div class="camera-box">
        <img 
            src="http://127.0.0.1:5000/video_feed"
            alt="Cámara PPE"
            onerror="this.style.display='none'; document.getElementById('cam-error').style.display='flex';">
        <div id="cam-error" class="camera-error">
            <h3>Cámara no disponible</h3>
            <p>No se pudo establecer conexión con el sistema de detección.</p>
        </div>
    </div>
</main>
</body>
</html>
