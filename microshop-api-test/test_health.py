import requests

def test_check_health():
    health_url = "http://127.0.0.1:8015/health"

    health_response = requests.get(
        url=health_url
    )

    health_body = health_response.json()

    assert health_response.status_code == 200

    assert health_body['status'] == 'ok'