# app.py
# Simple Flask API to return public IPv4 / IPv6 using ipify (server-side)
# Endpoints:
#   GET /api/ipv4 -> {"ip": "..."}
#   GET /api/ipv6 -> {"ip": "..."}

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import requests

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # allow requests from your index.html

TIMEOUT = 8
IPV4_URL = "https://api4.ipify.org?format=json"
IPV6_URL = "https://api6.ipify.org?format=json"

def get_ip(url: str):
    try:
        r = requests.get(url, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json() or {}
        return data.get("ip")
    except Exception:
        return None

@app.get("/api/ipv4")
def ipv4():
    return jsonify({"ip": get_ip(IPV4_URL)})

@app.get("/api/ipv6")
def ipv6():
    return jsonify({"ip": get_ip(IPV6_URL)})

# Optional: serve the HTML at /
@app.get("/")
def root():
    # Make sure index.html is in the same folder as testing.py
    return send_from_directory(".", "index.html")

if __name__ == "__main__":
    # Runs at http://127.0.0.1:5000/
    app.run(host="0.0.0.0", port=5000, debug=True)