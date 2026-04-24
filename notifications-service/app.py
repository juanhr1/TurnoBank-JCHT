from flask import Flask, request, jsonify
import psycopg2 # type: ignore
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
        print("Conectado a PostgreSQL")
        break
    except:
        print("Esperando BD...")
        time.sleep(3)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    identificacion VARCHAR(50),
    turno VARCHAR(20),
    mensaje TEXT
)
""")
conn.commit()


@app.route("/notify", methods=["POST"])
def notify():
    data = request.json

    identificacion = data["identificacion"]
    turno = data["turno"]
    mensaje = "Turno asignado: " + turno

    cur.execute(
        """
        INSERT INTO notifications
        (identificacion, turno, mensaje)
        VALUES (%s,%s,%s)
        """,
        (identificacion, turno, mensaje)
    )

    conn.commit()

    return jsonify({"mensaje": "Notificación guardada"})


@app.route("/notifications", methods=["GET"])
def get_notifications():

    cur.execute("""
        SELECT identificacion, turno, mensaje
        FROM notifications
    """)

    rows = cur.fetchall()

    lista = []

    for r in rows:
        lista.append({
            "identificacion": r[0],
            "turno": r[1],
            "mensaje": r[2]
        })

    return jsonify({
        "notificaciones": lista
    })


app.run(host="0.0.0.0", port=5000)