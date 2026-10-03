import requests

BASE_URL = "http://127.0.0.1:8015"

def send_request(method, path, **kwargs):
    """发送http请求，并返回完整响应对象"""
    # 请求层统一组合基础地址与业务API提供的path
    url = f"{BASE_URL}{path}"

    response = requests.request(
        method=method,
        url=url,
        **kwargs
    )

    return response