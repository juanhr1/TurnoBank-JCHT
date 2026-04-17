from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# USERS
@app.route("/users", methods=["GET"])
def get_users():
    response = requests.get("http://users-service:5000/users")
    return jsonify(response.json())

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    response = requests.post("http://users-service:5000/users", json=data)
    return jsonify(response.json())

# TURNS
@app.route("/turns", methods=["GET"])
def get_turns():
    response = requests.get("http://turns-service:5000/turns")
    return jsonify(response.json())

@app.route("/turn", methods=["POST"])
def create_turn():
    data = request.json
    response = requests.post("http://turns-service:5000/turn", json=data)
    return jsonify(response.json())

# NOTIFICATIONS
@app.route("/notifications", methods=["GET"])
def get_notifications():
    response = requests.get("http://notifications-service:5000/notifications")
    return jsonify(response.json())

@app.route("/notify", methods=["POST"])
def send_notification():
    data = request.json
    response = requests.post(
        "http://notifications-service:5000/notify",
        json=data
    )
    return jsonify(response.json())

@app.route("/")
def home():
    return jsonify({
        "mensaje": "API Gateway funcionando"
    })

app.run(host="0.0.0.0", port=5000)