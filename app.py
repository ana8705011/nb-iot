from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/datos', methods=['POST'])
def recibir_datos():
    contenido = request.json
    print(contenido)
    return 'OK', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
