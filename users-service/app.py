from flask import Flask, request, jsonify
import psycopg2 # type: ignore
import os
import time

app = Flask(__name__)

# CONEXION A BASE DE DATOS
while True:
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        cur = conn.cursor()

        print("Conectado a users_db")
        break

    except:
        print("Esperando base de datos...")
        time.sleep(3)

# CREAR TABLA
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    identificacion VARCHAR(50) UNIQUE,
    telefono VARCHAR(50)
)
""")
conn.commit()

# HOME
@app.route("/")
def home():
    return jsonify({
        "mensaje": "Users Service activo"
    })


# LISTAR USUARIOS
@app.route("/users", methods=["GET"])
def get_users():

    cur.execute("""
        SELECT id, identificacion, telefono
        FROM users
        ORDER BY id ASC
    """)

    rows = cur.fetchall()

    usuarios = []

    for r in rows:
        usuarios.append({
            "id": r[0],
            "identificacion": r[1],
            "telefono": r[2]
        })

    return jsonify({
        "mensaje": "Listado de usuarios",
        "usuarios_registrados": usuarios
    })

# CREAR USUARIO
@app.route("/users", methods=["POST"])
def create_user():

    data = request.json

    if not data:
        return jsonify({
            "error": "Debe enviar datos"
        }), 400

    if "identificacion" not in data:
        return jsonify({
            "error": "Falta identificacion"
        }), 400

    if "telefono" not in data:
        return jsonify({
            "error": "Falta telefono"
        }), 400

    identificacion = str(data["identificacion"])
    telefono = str(data["telefono"])

    # VALIDAR EXISTENCIA
    cur.execute("""
        SELECT * FROM users
        WHERE identificacion = %s
    """, (identificacion,))

    existe = cur.fetchone()

    if existe:
        return jsonify({
            "error": "Usuario ya existe"
        }), 409

    # INSERTAR
    cur.execute("""
        INSERT INTO users (identificacion, telefono)
        VALUES (%s, %s)
    """, (identificacion, telefono))

    conn.commit()

    print("Usuario creado:", identificacion)

    return jsonify({
        "mensaje": "Usuario registrado correctamente",
        "identificacion": identificacion,
        "telefono": telefono
    })

# INICIAR APP
app.run(host="0.0.0.0", port=5000)