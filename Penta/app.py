from flask import Flask, jsonify, send_from_directory, Response
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

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

@app.get("/speedtest")
def speedtest():
    size = 5 * 1024 * 1024   # 5 MB
    data = os.urandom(size)
    return Response(data, mimetype="application/octet-stream")


@app.get("/")
def root():
    return send_from_directory(".", "index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
