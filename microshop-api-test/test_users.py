# import requests
import uuid
import pytest

from api.users_api import (
    register_user,
    login_user,
    get_current_user
)

# API层已存在 下面地址可以删除
# BASE_URL = "http://127.0.0.1:8015"
# # 注册地址
# REGISTER_URL = f"{BASE_URL}/users/register"
# # 登录地址
# LOGIN_URL = f"{BASE_URL}/users/login"
# # 当前登录用户地址
# ME_URL = f"{BASE_URL}/users/me"

def test_register_user_success():
    """验证使用有效用户名和密码能够成功注册用户"""
    # 测试层负责准备本次注册场景所需的数据
    payload = {
        "username": f"user_{uuid.uuid4().hex[:8]}",
        "password": "test123456"
    }

    # API层负责发送请求，测试层接收完整响应
    success_response = register_user(payload)
    assert success_response.status_code == 201

    # 将JSON响应体解析为Python字典，供后续业务断言使用
    success_body = success_response.json()
    # 验证响应中的用户名等于请求中的用户名
    assert success_body["username"] == payload["username"]
    # 验证响应中存在id
    assert "id" in success_body
    # 验证响应中不存在password
    assert "password" not in success_body

def test_register_user_without_password_returns_422():
    """验证注册时缺少密码会返回参数校验错误"""
    payload = {
        "username": f"user_{uuid.uuid4().hex[:8]}",
    }

    # response = requests.post(
    #     url = REGISTER_URL,
    #     json = payload
    # )

    # API层负责发送注册请求
    response = register_user(payload)
    assert response.status_code == 422
    response_body = response.json()
    # 验证存在报错信息detail
    assert "detail" in response_body
    # 验证detail是列表
    assert isinstance(response_body["detail"], list)
    # 验证错误位置指向password字段
    assert response_body["detail"][0]["loc"][-1] == "password"
    # error_location = response_body["detail"][0]["loc"][-1]
    # assert error_location

def test_login_with_registered_user_success():
    """验证新注册用户能够成功登录并获得访问令牌"""
    payload = {
        "username": f"user_{uuid.uuid4().hex[:8]}",
        "password": "test123456"
    }

    # 通过API层注册前置用户
    register_response = register_user(payload)
    # 验证用户注册成功，确保登录前置数据准备完成
    assert register_response.status_code == 201

    # 通过API层发送登录请求
    login_response = login_user(payload)
    # 验证使用已注册的账号能够成功登录
    assert login_response.status_code == 200

    login_body = login_response.json()
    # 验证登录响应中存在访问令牌字段
    assert "access_token" in login_body
    # 验证访问令牌的类型是字符串
    assert isinstance(login_body["access_token"], str)
    # 验证访问令牌内容不为空
    assert login_body["access_token"]
    # 验证服务器返回令牌类型为bearer
    assert login_body["token_type"] == "bearer"

    # # 先注册唯一用户 为登录测试准备账号
    # register_response = requests.post(
    #     url=REGISTER_URL,
    #     json=credentials
    # )

    # # 使用同一组账号密码登录
    # login_response = requests.post(
    #     url=LOGIN_URL,
    #     json=credentials
    # )


def test_get_current_user_with_token_success(login_token):
    """验证用户登录后携带访问令牌能够获取到当前用户信息"""
    # 使用 fixture 返回的 Token 构造鉴权请求头
    # auth_headers = {
    #     "Authorization": f"Bearer {login_token}"
    # }
    # response = requests.get(
    #     headers=auth_headers,
    #     url=ME_URL
    # )

    # fixture提供Token，API层构造鉴权请求头并发送请求
    response = get_current_user(login_token)
    assert response.status_code == 200

    body = response.json()
    assert "id" in body
    assert "password" not in body

def test_get_current_user_without_authorization():
    """验证未携带认证凭证访问当前用户接口时的真实行为。"""
    # response = requests.get(
    #     url=ME_URL
    # )

    # 不传token API层将发送不带Authorization的请求头
    response = get_current_user()
    # 验证未携带认证凭证时返回实际观察到的状态码
    assert response.status_code == 401

    response_body = response.json()
    # 验证错误信息明确说明缺少 Bearer Token
    assert response_body["detail"] == "缺少 Bearer Token"

def test_get_current_user_with_invalid_token():
    """验证携带非法 Token 访问当前用户接口时的真实行为。"""
    # 构造包含明显错误 Bearer Token 的请求头
    # invalid_auth_headers = {
    #     "Authorization": "Bearer wrong_token"
    # }
    # 携带非法 Token 访问当前用户接口
    # response = requests.get(
    #     url=ME_URL,
    #     headers=invalid_auth_headers
    # )

    # 测试层负责准备当前异常场景所需要的无效token
    invalid_token = "wrong_token"
    # API层负责将非法token放入Bearer请求头并发送请求
    response = get_current_user(invalid_token)
    assert response.status_code == 401
    response_body = response.json()
    assert response_body["detail"] == "Token 无效或已过期"


@pytest.mark.parametrize(
    "payload, expected_status, expected_detail",
    [
        (
                {
                    "username":"",
                    "password":"test123456"
                },
            400,
            "用户名不能为空"
        ),
        (
                {
                    "username":f"user_{uuid.uuid4().hex[:8]}",
                    "password":""
                },
            400,
            "密码长度不能少于 6 位"
        ),
        (
                {
                    "username":f"user_{uuid.uuid4().hex[:8]}",
                    "password":"12345"
                },
            400,
            "密码长度不能少于 6 位"
        )
    ],
    ids=[
        "empty_username",
        "empty_password",
        "password_too_short"
    ]
)

def test_register_user_invalid(payload, expected_status, expected_detail):
    """验证多组无效注册数据均返回对应的业务校验错误"""
    # 使用当前参数组合发送注册请求
    # response = requests.post(
    #     url=REGISTER_URL,
    #     json=payload
    # )

    # API层使用当前参数组合发送注册请求
    response = register_user(payload)

    # 验证本组数据对应的预期状态码
    assert response.status_code == expected_status
    # 将 JSON 响应体解析为 Python 数据
    response_body = response.json()
    # 验证本组数据对应的错误详情
    assert response_body["detail"] == expected_detail

