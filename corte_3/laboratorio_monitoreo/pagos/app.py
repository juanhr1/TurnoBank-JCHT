from flask import Flask, jsonify
import time

app = Flask(__name__)

pagos_db = [
    {
        "id": 1,
        "cliente": "María Torres",
        "metodo_pago": "Tarjeta Crédito",
        "estado": "Aprobado"
    },
    {
        "id": 2,
        "cliente": "Juan Herrera",
        "metodo_pago": "Nequi",
        "estado": "Pendiente"
    },
    {
        "id": 3,
        "cliente": "Sofía Ramírez",
        "metodo_pago": "PSE",
        "estado": "Aprobado"
    }
]

@app.route("/")
def home():
    return "Servicio de pagos funcionando"

@app.route("/pagos")
def pagos():
    inicio = time.time()
    print("[PAGOS] Procesando pagos", flush=True)
    time.sleep(2)
    fin = time.time()
    print(f"[PAGOS] Tiempo de respuesta: {fin-inicio}", flush=True)
    return jsonify(pagos_db)

@app.route("/health")
def health():
    return {
        "status": "ok",
        "service": "pagos"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)