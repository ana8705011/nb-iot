from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Configuración de InfluxDB
INFLUX_URL = "https://deae-37-12-57-52.ngrok-free.app"
INFLUX_BUCKET = "IoT_influx"
INFLUX_ORG = "IES Andres Laguna"  # Puedes confirmar el nombre exacto de tu organización si da error
INFLUX_TOKEN = "IoT_influx"  # Sustituye por el token que aparece en InfluxDB

@app.route('/datos', methods=['POST'])
def recibir_datos():
    datos = request.json

    temperatura = datos.get('temperatura')
    humedad = datos.get('humedad')

    if temperatura is None or humedad is None:
        return "Faltan datos", 400

    # Construcción del Line Protocol
    line = f"sensores temperatura={temperatura},humedad={humedad}"

    # Enviar a InfluxDB
    response = requests.post(
        f"{INFLUX_URL}/api/v2/write?org={INFLUX_ORG}&bucket={INFLUX_BUCKET}&precision=s",
        data=line,
        headers={
            "Authorization": f"Token {INFLUX_TOKEN}",
            "Content-Type": "text/plain"
        }
    )

    print("Respuesta Influx:", response.status_code, response.text)
    return "Datos recibidos", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
