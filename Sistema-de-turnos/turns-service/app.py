from flask import Flask, request, jsonify
import psycopg2 # type: ignore
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
        print("Conectado a turns_db")
        break
    except:
        print("Esperando base de datos...")
        time.sleep(3)

cur = conn.cursor()

# CREAR TABLA
cur.execute("""
CREATE TABLE IF NOT EXISTS turns (
    id SERIAL PRIMARY KEY,
    identificacion VARCHAR(50),
    turno VARCHAR(20)
)
""")
conn.commit()

# HOME
@app.route("/")
def home():
    return jsonify({
        "mensaje": "Turns Service activo"
    })

# LISTAR TURNOS
@app.route("/turns", methods=["GET"])
def listar_turnos():

    cur.execute("""
        SELECT id, identificacion, turno
        FROM turns
        ORDER BY id ASC
    """)

    rows = cur.fetchall()

    lista = []

    for r in rows:
        lista.append({
            "id": r[0],
            "identificacion": r[1],
            "turno": r[2]
        })

    return jsonify({
        "mensaje": "Listado de turnos",
        "turnos": lista
    })

# CREAR TURNO
@app.route("/turn", methods=["POST"])
def crear_turno():

    data = request.json

    if not data or "identificacion" not in data:
        return jsonify({
            "error": "Debe enviar identificacion"
        }), 400

    identificacion = data["identificacion"]

    # VALIDAR USUARIO CON TIMEOUT
    try:
        response = requests.get(
            "http://users-service:5000/users",
            timeout=3
        )

        usuarios = response.json()["usuarios_registrados"]

    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Timeout consultando users-service"
        }), 504

    except:
        return jsonify({
            "error": "users-service no disponible"
        }), 500

    existe = False

    for u in usuarios:
        if str(u["identificacion"]) == str(identificacion):
            existe = True
            break

    if not existe:
        return jsonify({
            "error": "Usuario no existe"
        }), 404

    # CONTADOR PERSISTENTE
    cur.execute("SELECT COUNT(*) FROM turns")
    total = cur.fetchone()[0] + 1

    turno_generado = "T" + str(total)

    # GUARDAR TURNO
    cur.execute("""
        INSERT INTO turns (identificacion, turno)
        VALUES (%s, %s)
    """, (identificacion, turno_generado))

    conn.commit()

    print("Turno creado:", turno_generado)

    # NOTIFICACION CON TIMEOUT
    try:
        requests.post(
            "http://notifications-service:5000/notify",
            json={
                "identificacion": identificacion,
                "turno": turno_generado
            },
            timeout=3
        )

    except requests.exceptions.Timeout:
        print("Timeout en notifications-service")

    except:
        print("notifications-service no disponible")

    return jsonify({
        "mensaje": "Turno creado correctamente",
        "identificacion": identificacion,
        "turno": turno_generado
    })

# INICIAR SERVIDOR
app.run(host="0.0.0.0", port=5000)