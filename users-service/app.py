from flask import Flask, request, jsonify
import psycopg2 # type: ignore
import os
import time

app = Flask(__name__)

# Conexión con reintento
while True:
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        print("Conectado a la base de datos")
        break
    except:
        print("Esperando la base de datos...")
        time.sleep(3)

cur = conn.cursor()

# crear tabla si no existe
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    identificacion VARCHAR(50),
    telefono VARCHAR(50)
)
""")
conn.commit()

# GET usuarios
@app.route("/users", methods=["GET"])
def get_users():
    cur.execute("SELECT identificacion, telefono FROM users")
    rows = cur.fetchall()

    users = []
    for r in rows:
        users.append({
            "identificacion": r[0],
            "telefono": r[1]
        })

    return jsonify({
        "mensaje": "Usuarios desde BD",
        "usuarios_registrados": users
    })

# POST usuario
@app.route("/users", methods=["POST"])
def create_user():
    data = request.json

    cur.execute(
        "INSERT INTO users (identificacion, telefono) VALUES (%s, %s)",
        (data["identificacion"], data["telefono"])
    )
    conn.commit()

    return jsonify({"mensaje": "usuario guardado en BD"})

app.run(host="0.0.0.0", port=5000)