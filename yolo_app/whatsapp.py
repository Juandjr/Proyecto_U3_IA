import requests
import os
import base64

INSTANCE_ID = "instance161552"
TOKEN = "tgobbeydfr0dtdgw"

def enviar_whatsapp_imagen(numero, mensaje, ruta_imagen):
    telefono = f"+593{numero}"
    url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/image"
    try:
        with open(ruta_imagen, "rb") as img_file:
            imagen_base64 = base64.b64encode(img_file.read()).decode('utf-8')
        payload = {
            "token": TOKEN,
            "to": telefono,
            "image": imagen_base64,
            "caption": mensaje
        }
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        r = requests.post(url, data=payload, headers=headers, timeout=30)
        print("WhatsApp con imagen enviado a:", telefono)
        print("Respuesta UltraMsg:", r.text)

    except Exception as e:
        print("Error enviando WhatsApp:", e)
