from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# HOME
@app.route("/")
def home():
    print("[LOG Gateway] Acceso principal")
    return jsonify({"mensaje": "API Gateway funcionando"})


# USERS
@app.route("/users", methods=["GET"])
def get_users():
    print("[LOG Gateway] GET /users")
    response = requests.get("http://users-service:5000/users")
    return jsonify(response.json())

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    print("[LOG Gateway] POST /users", data)

    response = requests.post(
        "http://users-service:5000/users",
        json=data
    )

    return jsonify(response.json())


# TURNS
@app.route("/turns", methods=["GET"])
def get_turns():
    print("[LOG Gateway] GET /turns")
    response = requests.get("http://turns-service:5000/turns")
    return jsonify(response.json())

@app.route("/turn", methods=["POST"])
def create_turn():
    data = request.json
    print("[LOG Gateway] POST /turn", data)

    response = requests.post(
        "http://turns-service:5000/turn",
        json=data
    )

    return jsonify(response.json())


# NOTIFICATIONS
@app.route("/notifications", methods=["GET"])
def get_notifications():
    print("[LOG Gateway] GET /notifications")
    response = requests.get("http://notifications-service:5000/notifications")
    return jsonify(response.json())

@app.route("/notify", methods=["POST"])
def send_notification():
    data = request.json
    print("[LOG Gateway] POST /notify", data)

    response = requests.post(
        "http://notifications-service:5000/notify",
        json=data
    )

    return jsonify(response.json())


app.run(host="0.0.0.0", port=5000)