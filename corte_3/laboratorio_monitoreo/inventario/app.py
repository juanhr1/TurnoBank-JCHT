from flask import Flask, jsonify
import time

app = Flask(__name__)

inventario_db = [
    {
        "id": 1,
        "producto": "Tablet Samsung",
        "stock": 12,
        "precio": 1200
    },
    {
        "id": 2,
        "producto": "Impresora HP",
        "stock": 8,
        "precio": 650
    },
    {
        "id": 3,
        "producto": "Disco SSD 1TB",
        "stock": 20,
        "precio": 420
    }
]

@app.route("/")
def home():
    return "Servicio de inventario funcionando"

@app.route("/inventario")
def inventario():
    inicio = time.time()
    print("[INVENTARIO] Consultando inventario", flush=True)
    time.sleep(1)
    fin = time.time()
    print("[INVENTARIO] Servicio de inventario funcionando correctamente - 200", flush=True)
    print(f"[INVENTARIO] Tiempo de respuesta: {fin-inicio}", flush=True)
    return (inventario_db)

@app.route("/health")
def health():
    return {
        "status": "ok",
        "service": "inventario"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)