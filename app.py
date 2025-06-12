from flask import Flask, request, jsonify
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

# URL de la base (la vas a pasar como variable de entorno en Render)
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

# Crear tabla si no existe
with get_conn() as conn:
    with conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS datos (
                id SERIAL PRIMARY KEY,
                dispositivo TEXT,
                temperatura REAL,
                humedad REAL,
                timestamp TIMESTAMP
            )
        ''')
        conn.commit()

@app.route('/api/datos', methods=['POST'])
def recibir_datos():
    data = request.json
    dispositivo = data.get('dispositivo', 'desconocido')
    temperatura = data.get('temperatura')
    humedad = data.get('humedad')
    timestamp = datetime.now()

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO datos (dispositivo, temperatura, humedad, timestamp)
                VALUES (%s, %s, %s, %s)
            ''', (dispositivo, temperatura, humedad, timestamp))
            conn.commit()

    return jsonify({"mensaje": "Datos guardados correctamente"}), 200

@app.route('/api/datos', methods=['GET'])
def ver_datos():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM datos ORDER BY id DESC LIMIT 10')
            columnas = [desc[0] for desc in cur.description]
            datos = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
    return jsonify(datos), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)