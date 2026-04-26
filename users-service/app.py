from flask import Flask, request, jsonify
import psycopg2
import os
import time

app = Flask(__name__)

while True:
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        break
    except:
        time.sleep(3)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
id SERIAL PRIMARY KEY,
identificacion VARCHAR(50),
telefono VARCHAR(50)
)
""")
conn.commit()

@app.route("/users", methods=["GET"])
def get_users():
    cur.execute("SELECT identificacion, telefono FROM users")
    rows = cur.fetchall()

    lista = []
    for r in rows:
        lista.append({
            "identificacion": r[0],
            "telefono": r[1]
        })

    return jsonify({"usuarios_registrados": lista})

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json

    cur.execute(
        "INSERT INTO users (identificacion, telefono) VALUES (%s,%s)",
        (data["identificacion"], data["telefono"])
    )
    conn.commit()

    return jsonify({"mensaje":"usuario creado"})

app.run(host="0.0.0.0", port=5000)