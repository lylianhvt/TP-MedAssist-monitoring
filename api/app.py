from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics
import json
import random
import time

app = Flask(__name__)
metrics = PrometheusMetrics(app)


@app.before_request
def start_timer():
    request._start_time = time.time()


@app.route("/health")
def health():
    return jsonify({"mysql": "ok", "redis": "ok"})


@app.route("/api/doctors")
def doctors():
    return jsonify([{"id": 1, "name": "Dr. House"}, {"id": 2, "name": "Dr. Grey"}])


@app.route("/api/consultations", methods=["GET", "POST"])
def consultations():
    if request.method == "POST":
        return jsonify({"status": "created"}), 201
    return jsonify([{"id": 1, "doctor": "Dr. House"}])


@app.route("/api/payment", methods=["GET", "POST"])
def payment():
    if random.random() < 0.05:
        return jsonify({"error": "payment failed"}), 500
    return jsonify({"status": "paid"})


@app.route("/api/webhook/alert", methods=["POST"])
def alert_webhook():
    payload = request.get_json(silent=True) or {}
    print(json.dumps({"event": "alertmanager_webhook", "payload": payload}), flush=True)
    return jsonify({"status": "received"}), 200


@app.after_request
def log_request(response):
    duration = round((time.time() - getattr(request, "_start_time", time.time())) * 1000, 2)
    entry = {
        "method": request.method,
        "endpoint": request.path,
        "status": response.status_code,
        "duration": duration,
        "remote_addr": request.headers.get("X-Forwarded-For", request.remote_addr),
    }
    print(json.dumps(entry), flush=True)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
