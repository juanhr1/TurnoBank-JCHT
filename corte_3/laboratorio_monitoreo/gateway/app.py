from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

errores_pagos = 0

@app.route("/pedidos")
def pedidos():
    inicio = time.time()
    print("[GATEWAY] Consultando servicio pedidos", flush=True)
    try:
        response = requests.get("http://pedidos:5000/pedidos", timeout=3)
        fin = time.time()
        print(f"[INFO] Tiempo pedidos: {fin-inicio}", flush=True)
        return jsonify(response.json())
    except:
        print("[ERROR] Servicio pedidos no disponible", flush=True)
        return jsonify({
            "error": "Servicio pedidos no disponible"
        }), 503

@app.route("/inventario")
def inventario():
    inicio = time.time()
    print("[GATEWAY] Consultando servicio inventario", flush=True)
    try:
        response = requests.get("http://inventario:5000/inventario", timeout=3)
        fin = time.time()
        print(f"[INFO] Tiempo inventario: {fin-inicio}", flush=True)
        return jsonify(response.json())
    except:
        print("[ERROR] Servicio inventario no disponible", flush=True)
        return jsonify({
            "error": "Servicio inventario no disponible"
        }), 503

@app.route("/pagos")
def pagos():
    global errores_pagos
    inicio = time.time()
    print("[GATEWAY] Consultando servicio pagos", flush=True)
    try:
        response = requests.get("http://pagos:5000/pagos", timeout=3)
        fin = time.time()
        print(f"[INFO] Tiempo pagos: {fin-inicio}", flush=True)
        return jsonify(response.json()), response.status_code
    except:
        errores_pagos += 1
        print(f"[ERROR] Servicio pagos caído - errores: {errores_pagos}", flush=True)
        return jsonify({
            "error": "Servicio pagos no disponible"
        }), 503

@app.route("/estado/pedidos")
def estado_pedidos():
    try:
        response = requests.get("http://pedidos:5000/health", timeout=2)
        return jsonify(response.json())
    except:
        return jsonify({
            "status": "down"
        }), 503

@app.route("/estado/inventario")
def estado_inventario():
    try:
        response = requests.get("http://inventario:5000/health", timeout=2)
        return jsonify(response.json())
    except:
        return jsonify({
            "status": "down"
        }), 503

@app.route("/estado/pagos")
def estado_pagos():
    try:
        response = requests.get("http://pagos:5000/health", timeout=2)
        return jsonify(response.json())
    except:
        return jsonify({
            "status": "down"
        }), 503

@app.route("/")
def home():
    return "Gateway funcionando"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)