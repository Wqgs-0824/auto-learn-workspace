import requests

from api.request_client import send_request


BASE_URL = "http://127.0.0.1:8015"
# 用户注册接口地址
REGISTER_URL = f"{BASE_URL}/users/register"
# 用户登录接口地址
LOGIN_URL = f"{BASE_URL}/users/login"
# 当前登录用户接口地址
ME_URL = f"{BASE_URL}/users/me"


def register_user(payload):
    """发送用户注册请求，并将完整响应交给测试层进行断言。"""
    response = requests.post(
        url=REGISTER_URL,
        json=payload
    )

    return response

def login_user(payload):
    """发送用户登录请求 并返回完整响应"""
    login_response = requests.post(
        url=LOGIN_URL,
        json=payload
    )
    return login_response

def get_current_user(token=None):
    """根据可选token查询当前用户 并返回完整响应"""
    # 不提供token时 不携带Authorization 请求头
    headers = None

    if token is not None:
        headers = {
            "Authorization": f"Bearer {token}"
        }

    me_response = requests.get(
        url=ME_URL,
        headers=headers
    )
    return me_response
