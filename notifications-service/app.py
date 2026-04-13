from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/notify", methods=["POST"])
def send_notification():
    data = request.json

    mensaje = f"Notificación enviada al usuario {data['identificacion']} para el turno {data['turno']}"

    print(mensaje)

    return jsonify({
        "mensaje": "Notificación enviada",
        "detalle": mensaje
    })

@app.route("/notifications", methods=["GET"])
def get_notifications():
    return jsonify({
        "mensaje": "Servicio de notificaciones funcionando"
    })

app.run(host="0.0.0.0", port=5000)