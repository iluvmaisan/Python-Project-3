import os
import sys

# make sure the parent folder (Penta/) is on sys.path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import app


def test_endpoints_return_200():
    client = app.test_client()

    # all your main endpoints should at least respond with 200
    for path in ["/", "/api/ipv4", "/api/ipv6", "/api/geo", "/ping", "/speedtest"]:
        res = client.get(path)
        assert res.status_code == 200
