from ultralytics import YOLO
import cv2
import torch
import time
import os
import requests
from flask import Flask, Response, jsonify
from flask_cors import CORS
from whatsapp import enviar_whatsapp_imagen
from pathlib import Path

BASE_DIR = Path(__file__).parent
expected = BASE_DIR / "create-model-version-3" / "runs" / "detect" / "train" / "weights" / "best.pt"
model_path = None
if expected.exists():
    model_path = str(expected)
else:
    found_best = list(BASE_DIR.rglob('best.pt'))
    if found_best:
        model_path = str(found_best[0])
    else:
        found_any = list(BASE_DIR.rglob('*.pt'))
        if found_any:
            model_path = str(found_any[0])
        else:
            alt = BASE_DIR.parent / 'yolov8n.pt'
            if alt.exists():
                model_path = str(alt)

if model_path is None:
    raise FileNotFoundError(
        'No se encontró un archivo .pt para el modelo. Coloque el modelo en ' +
        str(expected) + ' o en el directorio del proyecto.'
    )

print('Cargando modelo desde:', model_path)
model = YOLO(model_path)
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# Configuración de detección
CONF = 0.60
IOU = 0.70

# Clases
CLS_PERSON = "person"
REQ_EPP = ["hardhat", "safety-gloves", "safety-goggles", "safety-boots"]

# Alertas
ALERT_COOLDOWN_SEC = 1.5
last_alert_time_by_person = {}

# Envío WhatsApp global
ultima_alerta = 0
TIEMPO_ALERTA = 30
CARPETA_CAPTURAS = "capturas"
os.makedirs(CARPETA_CAPTURAS, exist_ok=True)

alerta_activa = False

def norm(s):
    return str(s).strip().lower()

def center_in_person(person_box, epp_box):
    px1, py1, px2, py2 = person_box
    ex1, ey1, ex2, ey2 = epp_box
    cx = (ex1 + ex2) / 2.0
    cy = (ey1 + ey2) / 2.0
    return (px1 <= cx <= px2) and (py1 <= cy <= py2)

use_gpu = torch.cuda.is_available()
print("Esta usando GPU con CUDA:", use_gpu)
print("CLASSES:", model.names)

app = Flask(__name__)
CORS(app)

def obtener_telefono_usuario():
    try:
        r = requests.get("http://localhost/InterfazProyecto/web/get_user_phone.php", timeout=2)
        telefono = r.text.strip()
        return telefono if telefono.isdigit() else None
    except:
        return None

def generar_frames():
    global ultima_alerta, alerta_activa
    telefono_usuario = None
    prev_time = 0

    while True:
        # leer frame
        ret, frame = camera.read()
        if not ret or frame is None:
            time.sleep(0.05)
            continue

        if telefono_usuario is None:
            telefono_usuario = obtener_telefono_usuario()

        # resize para mantener carga controlada
        h, w = frame.shape[:2]
        new_w = 960
        new_h = int(h * new_w / w)
        frame = cv2.resize(frame, (new_w, new_h))

        results = model.predict(
            frame,
            conf=CONF,
            iou=IOU,
            device=0 if use_gpu else "cpu",
            verbose=False
        )

        r = results[0]
        names = model.names

        persons = []
        epps = {k: [] for k in REQ_EPP}

        if r.boxes is not None and len(r.boxes) > 0:
            for b in r.boxes:
                cls_id = int(b.cls.item())
                label = norm(names[cls_id])

                x1, y1, x2, y2 = map(float, b.xyxy[0].tolist())
                box = (x1, y1, x2, y2)

                if label == norm(CLS_PERSON):
                    persons.append(box)
                elif label in {norm(x) for x in REQ_EPP}:
                    for k in REQ_EPP:
                        if label == norm(k):
                            epps[k].append(box)
                            break

        now = time.time()
        alerta_activa = False

        # CORRELACION: por cada persona, revisar EPP faltante
        for pbox in persons:
            missing = []

            for epp_name in REQ_EPP:
                matched = False
                for ebox in epps[epp_name]:
                    if center_in_person(pbox, ebox):
                        matched = True
                        break
                if not matched:
                    missing.append(epp_name)

            if missing:
                alerta_activa = True
                key = tuple(int(v // 15) for v in pbox)
                last_t = last_alert_time_by_person.get(key, 0.0)
                if (now - last_t) >= ALERT_COOLDOWN_SEC:
                    print(f"[ALERTA] Persona SIN EPP: faltan {missing}")
                    last_alert_time_by_person[key] = now

                    # enviar mensaje alerta a WhatsApp
                    if telefono_usuario and (now - ultima_alerta > TIEMPO_ALERTA):
                        nombre_img = f"{CARPETA_CAPTURAS}/alerta_epp_{int(now)}.jpg"
                        cv2.imwrite(nombre_img, frame)
                        try:
                            enviar_whatsapp_imagen(
                                telefono_usuario,
                                f"⚠️ ALERTA EPP:\nAlerta en Area LAB-06 bloque B alerta de posible falta de EPP\n",
                                nombre_img
                            )
                            ultima_alerta = now
                        except Exception as e:
                            print("Error enviando WhatsApp:", e)

        annotated_frame = r.plot()

        # FPS overlay
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
        prev_time = curr_time

        overlay_text = [
            f"FPS: {fps:.2f}",
            f"Resolucion: {new_w}x{new_h}",
            f"Device: {'GPU' if use_gpu else 'CPU'}",
            f"Persons: {len(persons)}",
            f"Alerta EPP: {int(alerta_activa)}"
        ]

        y0 = 30
        for i, text in enumerate(overlay_text):
            y = y0 + i * 30
            cv2.putText(
                annotated_frame,
                text,
                (10, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2,
                cv2.LINE_AA
            )

        _, buffer = cv2.imencode('.jpg', annotated_frame)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generar_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/status')
def status():
    return jsonify({"alerta": alerta_activa})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True, threaded=True, use_reloader=False)
