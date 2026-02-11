CREATE DATABASE ProyectoU3IA
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

USE ProyectoU3IA;

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado TINYINT(1) DEFAULT 1,
    activo TINYINT(1) DEFAULT 0
);

