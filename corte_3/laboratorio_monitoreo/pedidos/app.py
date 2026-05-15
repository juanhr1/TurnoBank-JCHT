from flask import Flask, jsonify
import time

app = Flask(__name__)

pedidos_db = [
    {
        "id": 1,
        "cliente": "Carlos Mendoza",
        "producto": "Monitor Gamer",
        "cantidad": 2
    },
    {
        "id": 2,
        "cliente": "Laura Gómez",
        "producto": "Auriculares Bluetooth",
        "cantidad": 1
    },
    {
        "id": 3,
        "cliente": "Andrés Ruiz",
        "producto": "Silla Ergonómica",
        "cantidad": 1
    }
]

@app.route("/")
def home():
    return "Servicio de pedidos funcionando"

@app.route("/pedidos")
def pedidos():
    inicio = time.time()
    print("[PEDIDOS] Consultando pedidos", flush=True)
    time.sleep(1)
    fin = time.time()
    print("[PEDIDOS] Servicio de pedidos funcionando correctamente - 200", flush=True)
    print(f"[PEDIDOS] Tiempo de respuesta: {fin-inicio}", flush=True)
    return jsonify(pedidos_db)

@app.route("/health")
def health():
    return {
        "status": "ok",
        "service": "pedidos"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)