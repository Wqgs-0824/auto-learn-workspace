
from api.health_api import get_health

def test_check_health():
    # health_url = f"{BASE_URL}/health"

    health_response = get_health()

    health_body = health_response.json()

    assert health_response.status_code == 200

    assert health_body['status'] == 'ok'