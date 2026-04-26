from flask import Flask, request, jsonify
import psycopg2
import os
import time
import requests

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
CREATE TABLE IF NOT EXISTS turns(
id SERIAL PRIMARY KEY,
identificacion VARCHAR(50),
turno VARCHAR(20)
)
""")
conn.commit()

@app.route("/turns", methods=["GET"])
def get_turns():
    cur.execute("SELECT identificacion, turno FROM turns")
    rows = cur.fetchall()

    lista = []
    for r in rows:
        lista.append({
            "identificacion": r[0],
            "turno": r[1]
        })

    return jsonify({"turnos": lista})

@app.route("/turn", methods=["POST"])
def create_turn():
    data = request.json
    identificacion = data["identificacion"]

    r = requests.get("http://users-service:5000/users")
    usuarios = r.json()["usuarios_registrados"]

    existe = False
    for u in usuarios:
        if u["identificacion"] == identificacion:
            existe = True

    if not existe:
        return jsonify({"error":"usuario no existe"}),400

    cur.execute("SELECT COUNT(*) FROM turns")
    total = cur.fetchone()[0] + 1
    turno = "T" + str(total)

    cur.execute(
        "INSERT INTO turns (identificacion, turno) VALUES (%s,%s)",
        (identificacion, turno)
    )
    conn.commit()

    requests.post(
        "http://notifications-service:5000/notify",
        json={
            "identificacion": identificacion,
            "turno": turno
        }
    )

    return jsonify({
        "identificacion": identificacion,
        "turno": turno
    })

app.run(host="0.0.0.0", port=5000)