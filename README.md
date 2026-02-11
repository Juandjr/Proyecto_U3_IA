# Proyecto_U3_IA  
## Sistema de Detección de Equipamiento PPE con YOLOv8

Este proyecto consiste en una aplicación web integrada con un sistema de detección de objetos mediante YOLOv8, capaz de identificar el uso correcto de Equipos de Protección Personal (PPE) en tiempo real.

El sistema combina:

- Backend en Python (YOLOv8 + OpenCV)
- Interfaz Web (HTML, CSS, JS, PHP)
- Base de datos (MySQL / SQL Server)
- Sistema de alertas

---

# Instrucciones de Ejecución

IMPORTANTE:  
Primero debe ejecutarse el sistema de detección en Python antes de ingresar a la página web.

---

## Paso 1 — Ejecutar el sistema de detección

1. Abrir una terminal.
2. Navegar hasta la carpeta del proyecto:

```bash
cd yolo_app
```

3. (Opcional) Activar entorno virtual:

```bash
venv\Scripts\activate
```

4. Ejecutar el archivo principal:

```bash
python detection.py
```

Si todo está correcto:

- Se abrirá la cámara.
- El modelo YOLO comenzará la detección en tiempo real.
- El sistema quedará listo para enviar información a la interfaz web.

---

## Paso 2 — Ingresar a la aplicación web

1. Iniciar XAMPP (Apache y MySQL).
2. Abrir el navegador.
3. Ingresar a:

```
http://localhost/InterfazProyecto/web
```

4. Iniciar sesión con un usuario registrado.
5. Acceder a la interfaz principal.

---

# Funcionamiento del Sistema

- El modelo YOLO analiza la cámara en tiempo real.
- Si detecta incumplimiento del uso de PPE:
  - Se genera una alerta.
  - Se puede enviar una notificación (según configuración).
- Si detecta cumplimiento correcto:
  - Se muestra estado normal en pantalla.

---

# Tecnologías Utilizadas

- Python
- YOLOv8 (Ultralytics)
- OpenCV
- HTML5
- CSS3
- JavaScript
- PHP
- MySQL / SQL Server
- Bootstrap

---

# Estructura del Proyecto

```
Proyecto_U3_IA/
│
├── web/       # Sistema web (Login, Registro, Dashboard)
├── yolo_app/               # Sistema de detección
│   ├── detection.py
│   ├── whatsapp.py
│   └── modelo
├── sql/
└── README.md
```

---

# Requisitos

- Python 3.9 o superior
- XAMPP
- Librerías necesarias:

```bash
pip install ultralytics opencv-python numpy flask
```

(O usar `requirements.txt` si está disponible)

---

# Notas Importantes

- El archivo `detection.py` debe estar ejecutándose antes de ingresar a la web.
- Los archivos `.pt` (modelos YOLO) no están incluidos en el repositorio debido a su tamaño.
- Asegúrese de colocar el modelo entrenado en la carpeta correspondiente antes de ejecutar el sistema.
