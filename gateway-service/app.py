from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

TIMEOUT = 3

fallos_users = 0
circuito_users = False

estado_users = "CLOSED"

tiempo_apertura_users = 0

tiempo_espera = 10

# HOME
@app.route("/")
def home():
    return jsonify({
        "mensaje": "API Gateway funcionando",
        "servicios": [
            "users-service",
            "turns-service",
            "notifications-service"
        ]
    })

# USERS - GET
@app.route("/users", methods=["GET"])
def get_users():
    global fallos_users, circuito_users, estado_users, tiempo_apertura_users

    if circuito_users:
        tiempo_actual = time.time()
        if tiempo_actual - tiempo_apertura_users >= tiempo_espera:
            estado_users = "HALF-OPEN"
            circuito_users = False
            print("Users en estado HALF-OPEN → probando reconexión", flush=True)
        else:
            print("Circuito users abierto → bloqueando llamadas", flush=True)
            print("Esperando reconexión users... reintento en 10 segundos", flush=True)
            return jsonify({"error": "Circuito users abierto"}), 503

    try:
        response = requests.get("http://users-service:5000/users", timeout=TIMEOUT)
        fallos_users = 0
        if estado_users == "HALF-OPEN":
            print("Servicio users recuperado, se cierra el circuito", flush=True)
        else:
            print("Circuito cerrado en el servicio de usuarios", flush=True)
        circuito_users = False
        estado_users = "CLOSED"
        return jsonify(response.json())

    except:
        fallos_users += 1
        print(f"Fallo users número {fallos_users}", flush=True)
        if estado_users == "HALF-OPEN":
            circuito_users = True
            estado_users = "OPEN"
            tiempo_apertura_users = time.time()
            print("HALF-OPEN de users falló, por tanto se reabre el circuito", flush=True)
            return jsonify({"error": "users-service no disponible"}), 503

        if fallos_users >= 3:
            circuito_users = True
            estado_users = "OPEN"
            tiempo_apertura_users = time.time()
            print("Circuito users abierto → servicio no disponible temporalmente", flush=True)

        return jsonify({"error": "users-service no disponible"}), 503


# USERS - POST
@app.route("/users", methods=["POST"])
def create_user():

    try:
        data = request.json

        response = requests.post(
            "http://users-service:5000/users",
            json=data,
            timeout=TIMEOUT
        )

        return jsonify(response.json())

    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Timeout en users-service"
        }), 504

    except:
        return jsonify({
            "error": "users-service no disponible"
        }), 500


# TURNS - GET
@app.route("/turns", methods=["GET"])
def get_turns():

    try:
        response = requests.get(
            "http://turns-service:5000/turns",
            timeout=TIMEOUT
        )

        return jsonify(response.json())

    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Timeout en turns-service"
        }), 504

    except:
        return jsonify({
            "error": "turns-service no disponible"
        }), 500


# TURNS - POST
@app.route("/turn", methods=["POST"])
def create_turn():

    try:
        data = request.json

        response = requests.post(
            "http://turns-service:5000/turn",
            json=data,
            timeout=TIMEOUT
        )

        return jsonify(response.json())

    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Timeout en turns-service"
        }), 504

    except:
        return jsonify({
            "error": "turns-service no disponible"
        }), 500


# NOTIFICATIONS - GET
@app.route("/notifications", methods=["GET"])
def get_notifications():

    try:
        response = requests.get(
            "http://notifications-service:5000/notifications",
            timeout=TIMEOUT
        )

        return jsonify(response.json())

    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Timeout en notifications-service"
        }), 504

    except:
        return jsonify({
            "error": "notifications-service no disponible"
        }), 500


# NOTIFICATIONS - POST
@app.route("/notify", methods=["POST"])
def send_notification():

    try:
        data = request.json

        response = requests.post(
            "http://notifications-service:5000/notify",
            json=data,
            timeout=TIMEOUT
        )

        return jsonify(response.json())

    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Timeout en notifications-service"
        }), 504

    except:
        return jsonify({
            "error": "notifications-service no disponible"
        }), 500


# INICIAR APP
app.run(host="0.0.0.0", port=5000)