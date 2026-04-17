from flask import Flask, request, jsonify

app = Flask(__name__)

notificaciones = []

# Recibir notificación
@app.route("/notify", methods=["POST"])
def notify():
    data = request.json

    notificacion = {
        "identificacion": data["identificacion"],
        "turno": data["turno"],
        "mensaje": f"Turno asignado: {data['turno']}"
    }

    notificaciones.append(notificacion)

    print("Notificación recibida:", notificacion)

    return jsonify({"mensaje": "Notificación enviada correctamente"})

# Listar notificaciones
@app.route("/notifications", methods=["GET"])
def get_notifications():
    return jsonify({
        "mensaje": "Listado de notificaciones",
        "notificaciones": notificaciones
    })

app.run(host="0.0.0.0", port=5000)