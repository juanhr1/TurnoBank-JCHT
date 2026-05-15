from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

errores_pedidos = 0
errores_inventario = 0
errores_pagos = 0

@app.route("/pedidos")
def pedidos():
    global errores_pedidos
    inicio = time.time()
    print("[GATEWAY] Consultando servicio pedidos", flush=True)
    try:
        response = requests.get("http://pedidos:5000/pedidos", timeout=3)
        fin = time.time()
        print("[GATEWAY] Servicio de pedidos funcionando correctamente - 200", flush=True)
        print(f"[INFO] Tiempo pedidos: {fin-inicio}", flush=True)
        return jsonify(response.json())

    except:
        errores_pedidos += 1
        print(f"[ERROR] Servicio pedidos caído - errores: {errores_pedidos}", flush=True)
        return jsonify({
            "error": "Servicio pedidos no disponible",
            "fallos": errores_pedidos
        }), 503

@app.route("/inventario")
def inventario():
    global errores_inventario
    inicio = time.time()
    print("[GATEWAY] Consultando servicio inventario", flush=True)
    try:
        response = requests.get("http://inventario:5000/inventario", timeout=3)
        fin = time.time()
        print("[GATEWAY] Servicio de inventario funcionando correctamente - 200", flush=True)
        print(f"[INFO] Tiempo inventario: {fin-inicio}", flush=True)
        return jsonify(response.json())
    except:
        errores_inventario += 1
        print(f"[ERROR] Servicio inventario caído - errores: {errores_inventario}", flush=True)
        return jsonify({
            "error": "Servicio inventario no disponible",
            "fallos": errores_inventario
        }), 503

@app.route("/pagos")
def pagos():
    global errores_pagos
    inicio = time.time()
    print("[GATEWAY] Consultando servicio pagos", flush=True)
    try:
        response = requests.get("http://pagos:5000/pagos", timeout=3)
        fin = time.time()
        print("[GATEWAY] Servicio de pagos funcionando correctamente - 200", flush=True)
        print(f"[INFO] Tiempo pagos: {fin-inicio}", flush=True)
        return jsonify(response.json()), response.status_code
    except:
        errores_pagos += 1
        print(f"[ERROR] Servicio pagos caído - errores: {errores_pagos}", flush=True)
        return jsonify({
            "error": "Servicio pagos no disponible"
            "fallos": errores_pagos
        }), 503

@app.route("/estado/pedidos")
def estado_pedidos():
    global errores_pedidos
    inicio = time.time()
    print("[MONITOREO] Consultando estado pedidos", flush=True)
    try:
        response = requests.get("http://pedidos:5000/health", timeout=2)
        fin = time.time()
        print("[MONITOREO] Pedidos funcionando correctamente - 200", flush=True)
        print(f"[INFO] Tiempo estado pedidos: {fin-inicio}", flush=True)
        return jsonify(response.json())
    except:
        errores_pedidos += 1
        print(f"[ERROR] Estado del servicio de pedidos -> no disponible - errores: {errores_pedidos}", flush=True)
        return jsonify({
            "status": "down",
            "fallos": errores_pedidos
        }), 503

@app.route("/estado/inventario")
def estado_inventario():
    global errores_inventario
    inicio = time.time()
    print("[MONITOREO] Consultando estado inventario", flush=True)
    try:
        response = requests.get("http://inventario:5000/health", timeout=2)
        fin = time.time()
        print("[MONITOREO] Inventario funcionando correctamente - 200", flush=True)
        print(f"[INFO] Tiempo estado inventario: {fin-inicio}", flush=True)
        return jsonify(response.json())
    except:
        errores_inventario += 1
        print(f"[ERROR] Estado del servicio de inventario -> no disponible - errores: {errores_inventario}", flush=True)
        return jsonify({
            "status": "down",
            "fallos": errores_inventario
        }), 503

@app.route("/estado/pagos")
def estado_pagos():
    global errores_pagos
    inicio = time.time()
    print("[MONITOREO] Consultando estado pagos", flush=True)
    try:
        response = requests.get("http://pagos:5000/health", timeout=2)
        fin = time.time()
        print("[MONITOREO] Pagos funcionando correctamente - 200", flush=True)
        print(f"[INFO] Tiempo estado pagos: {fin-inicio}", flush=True)
        return jsonify(response.json())
    except:
        errores_pagos += 1
        print(f"[ERROR] Estado del servicio de pagos -> no disponible - errores: {errores_pagos}", flush=True)
        return jsonify({
            "status": "down",
            "fallos": errores_pagos
        }), 503

@app.route("/")
def home():
    return "Gateway funcionando"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)