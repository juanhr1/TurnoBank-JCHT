from flask import Flask, request, jsonify
import requests
import psycopg2 # pyright: ignore[reportMissingModuleSource]
import os
import time

app = Flask(__name__)

# Conexión a BD
while True:
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        print("[LOG Turns] Conectado a PostgreSQL")
        break
    except:
        print("[LOG Turns] Esperando base de datos...")
        time.sleep(3)

cur = conn.cursor()

# Crear tabla
cur.execute("""
CREATE TABLE IF NOT EXISTS turns (
    id SERIAL PRIMARY KEY,
    identificacion VARCHAR(50),
    turno VARCHAR(20)
)
""")
conn.commit()

print("[LOG Turns] Tabla turns verificada")

contador = 1


# POST crear turno
@app.route("/turn", methods=["POST"])
def crear_turno():
    global contador

    data = request.json
    identificacion = data["identificacion"]

    print("[LOG Turns] Solicitud de turno para:", identificacion)

    # Validar usuario
    try:
        response = requests.get("http://users-service:5000/users")
        users = response.json()["usuarios_registrados"]

        existe = False

        for u in users:
            if str(u["identificacion"]) == str(identificacion):
                existe = True
                break

        if not existe:
            print("[LOG Turns] Usuario no existe")
            return jsonify({"error": "El usuario no existe"}), 400

    except:
        print("[LOG Turns] Error conectando users-service")
        return jsonify({"error": "Error con users-service"}), 500

    # Crear turno
    turno_id = "T" + str(contador)
    contador += 1

    cur.execute(
        "INSERT INTO turns (identificacion, turno) VALUES (%s,%s)",
        (identificacion, turno_id)
    )
    conn.commit()

    print("[LOG Turns] Turno guardado:", turno_id)

    # Enviar notificación
    try:
        requests.post(
            "http://notifications-service:5000/notify",
            json={
                "identificacion": identificacion,
                "turno": turno_id
            }
        )

        print("[LOG Turns] Notificación enviada")

    except:
        print("[LOG Turns] Error enviando notificación")

    return jsonify({
        "identificacion": identificacion,
        "turno": turno_id
    })


# GET turnos
@app.route("/turns", methods=["GET"])
def listar_turnos():

    print("[LOG Turns] Consultando turnos")

    cur.execute("SELECT identificacion, turno FROM turns")
    rows = cur.fetchall()

    turnos = []

    for r in rows:
        turnos.append({
            "identificacion": r[0],
            "turno": r[1]
        })

    return jsonify({
        "mensaje": "Turnos desde BD",
        "turnos": turnos
    })


app.run(host="0.0.0.0", port=5000)