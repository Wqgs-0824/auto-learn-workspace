import requests

from config import BASE_URL

def test_check_health():
    health_url = f"{BASE_URL}/health"

    health_response = requests.get(
        url=health_url
    )

    health_body = health_response.json()

    assert health_response.status_code == 200

    assert health_body['status'] == 'ok'