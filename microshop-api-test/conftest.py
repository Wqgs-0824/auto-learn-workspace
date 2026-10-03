import pytest
import requests
import uuid

from api.users_api import (
    register_user,
    login_user,
    get_current_user
)

# BASE_URL = "http://127.0.0.1:8015"
# # 注册地址
# REGISTER_URL = f"{BASE_URL}/users/register"
# # 登录地址
# LOGIN_URL = f"{BASE_URL}/users/login"

@pytest.fixture(scope="module")
def login_token():
    """为每个测试模块注册并登录一个临时用户 返回共享Token"""
    # 创建唯一用户，避免重复运行测试时用户名冲突
    payload = {
        "username": f"user_{uuid.uuid4().hex[:8]}",
        "password": "test123456"
    }
    # API层负责发送注册请求
    register_response = register_user(payload)
    # fixture检查前置注册是否成功
    assert register_response.status_code == 201

    # API层负责发送登录请求
    login_response = login_user(payload)
    # fixture 检查前置登录是否成功
    assert login_response.status_code == 200

    # fixture解析响应并提取测试需要的token
    login_body = login_response.json()
    token = login_body["access_token"]

    return token

    # register_response = requests.post(
    #     url=REGISTER_URL,
    #     json=payload
    # )

    # # 使用刚注册的账号登录并提取 Token
    # login_response = requests.post(
    #     url=LOGIN_URL,
    #     json=payload
    # )
    # assert login_response.status_code == 200
    # login_body = login_response.json()
    # token = login_body["access_token"]
    #
    # return token
