from app import app

def test_endpoints_return_200():
    client = app.test_client()

    # all your main endpoints should at least respond with 200
    for path in ["/", "/api/ipv4", "/api/ipv6", "/api/geo", "/ping", "/speedtest"]:
        res = client.get(path)
        assert res.status_code == 200
