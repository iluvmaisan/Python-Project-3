from flask import Flask, jsonify, send_from_directory, Response
from flask_cors import CORS
import requests
import os
import time

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

TIMEOUT = 8
IPV4_URL = "https://api4.ipify.org?format=json"
IPV6_URL = "https://api6.ipify.org?format=json"

GEO_URL = "https://ipwhois.app/json/{}"


def get_ip(url: str):
    try:
        r = requests.get(url, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json() or {}
        return data.get("ip")
    except Exception:
        return None


def get_geo(ip):
    try:
        r = requests.get(GEO_URL.format(ip), timeout=TIMEOUT)
        r.raise_for_status()
        return r.json() or {}
    except Exception:
        return {}


@app.get("/api/ipv4")
def ipv4():
    return jsonify({"ip": get_ip(IPV4_URL)})


@app.get("/api/ipv6")
def ipv6():
    return jsonify({"ip": get_ip(IPV6_URL)})


# 🚀 NEW — Geolocation endpoint
@app.get("/api/geo")
def geo():
    ip = get_ip(IPV4_URL)
    raw = get_geo(ip)

    return jsonify({
        "ip": ip,
        "country_name": raw.get("country"),
        "region": raw.get("region"),
        "city": raw.get("city"),
        "org": raw.get("isp"),
        "asn": raw.get("asn"),
        "timezone": raw.get("timezone")
    })


@app.get("/speedtest")
def speedtest():
    size = 5 * 1024 * 1024   # 5 MB
    data = os.urandom(size)
    return Response(data, mimetype="application/octet-stream")


@app.get("/ping")
def ping():
    start = time.time()
    return jsonify({"time": round((time.time() - start) * 1000, 2)})


@app.get("/")
def root():
    return send_from_directory(".", "index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
