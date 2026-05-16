from flask import Flask, request, jsonify
import psycopg2
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

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    identificacion VARCHAR(50) UNIQUE,
    telefono VARCHAR(50)
)
""")
conn.commit()

@app.route("/")
def home():
    return jsonify({"mensaje": "Servicio de usuarios funcionando correctamente"})

@app.route("/users", methods=["GET"])
def get_users():
    inicio = time.time()
    print("[USERS] Consultando usuarios", flush=True)
    cur.execute("""
        SELECT id, identificacion, telefono
        FROM users
        ORDER BY id ASC""")
    rows = cur.fetchall()
    usuarios = []
    for r in rows:
        usuarios.append({
            "id": r[0],
            "identificacion": r[1],
            "telefono": r[2]
        })
    fin = time.time()
    print("[USERS] Servicio funcionando correctamente - 200", flush=True)
    print(f"[INFO] Tiempo de consulta de usuarios: {fin-inicio}", flush=True)
    return jsonify({
        "mensaje": "Listado de usuarios",
        "usuarios_registrados": usuarios
    })

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    if not data:
        return jsonify({
            "error": "Solicitud inválida"
            "detalle": "Debe ingresar los datos"
            }), 400
    if "identificacion" not in data:
        return jsonify({
            "error": "Campo requerido"
            "detalle": "El campo identificación es obligatorio"
            }), 400
    if "telefono" not in data:
        return jsonify({
            "error": "Campo requerido",
            "detalle": "El campo telefono es obligatorio"
            }), 400
    identificacion = str(data["identificacion"])
    telefono = str(data["telefono"])
    if not identificacion.isdigit():
        return jsonify({
            "error": "Dato inválido",
            "detalle": "La identificación debe ser un únicamente numérica"
            }), 400
    cur.execute("""
        SELECT * FROM users
        WHERE identificacion = %s
    """, (identificacion,))
    existe = cur.fetchone()
    if existe:
        return jsonify({
            "error": "Usuario ya existe"
            "detalle": "Ya existe un usuario registrado con esa identificación"
        }), 409
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
    }), 201

@app.route("/health")
def health():
    print("Verificando estado del servicio de usuarios...", flush=True)
    return jsonify({
        "status": "ok"
        "service": "users-service"
    }), 200

# INICIAR APP
app.run(host="0.0.0.0", port=5000)