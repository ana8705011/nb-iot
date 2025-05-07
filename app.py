from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Configuración de InfluxDB
INFLUX_URL = "https://deae-37-12-57-52.ngrok-free.app"
INFLUX_BUCKET = "IoT_influx"
INFLUX_ORG = "IES Andres Laguna"
INFLUX_TOKEN = "emlvuP88NQhrvPDM0uquWPi4LRbY2S0CKFD-6-IoI5QRYK9ea_Q9Gedsy7dkKcu6MMi9ekSAeL3Mpwxzd_z07A=="

@app.route('/datos', methods=['POST'])
def recibir_datos():
    datos = request.json
    print("Datos recibidos:", datos)

    temperatura = datos.get('temperatura')
    humedad = datos.get('humedad')
    dispositivo = datos.get('dispositivo', 'sin_nombre')

    if temperatura is None or humedad is None:
        return "Faltan datos", 400

    try:
        # Construcción del Line Protocol con etiqueta "dispositivo"
        line = f'sensores,dispositivo={dispositivo} temperatura={temperatura},humedad={humedad}'

        response = requests.post(
            f"{INFLUX_URL}/api/v2/write?org={INFLUX_ORG}&bucket={INFLUX_BUCKET}&precision=s",
            data=line,
            headers={
                "Authorization": f"Token {INFLUX_TOKEN}",
                "Content-Type": "text/plain"
            }
        )

        print("Respuesta Influx:", response.status_code, response.text)

        if response.status_code != 204:
            return f"Error al enviar a InfluxDB: {response.text}", 500

        return "Datos enviados correctamente a InfluxDB", 200

    except Exception as e:
        print("Error:", e)
        return "Error interno del servidor", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
