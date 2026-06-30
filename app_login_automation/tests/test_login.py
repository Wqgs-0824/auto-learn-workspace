"""APP 登录 UI 自动化测试用例。"""
import pytest

from pages.login_page import LoginPage


class TestLogin:
    """登录功能测试集。"""

    def test_login_success(self, driver, config):
        """正确的用户名和密码 -> 登录成功，进入首页。"""
        account = config["account"]["valid"]
        login_page = LoginPage(driver)
        login_page.login(account["username"], account["password"])

        assert login_page.is_login_success(), "使用正确账号登录后未进入首页"

    def test_login_wrong_password(self, driver, config):
        """错误的密码 -> 登录失败，出现错误提示。"""
        account = config["account"]["invalid"]
        login_page = LoginPage(driver)
        login_page.login(account["username"], account["password"])

        assert login_page.is_error_shown(), "密码错误时未出现错误提示"
        assert not login_page.is_login_success(), "密码错误却登录成功了"

    @pytest.mark.parametrize(
        "username, password",
        [
            ("", "Test@123456"),   # 用户名为空
            ("test_user", ""),     # 密码为空
            ("", ""),              # 都为空
        ],
    )
    def test_login_empty_input(self, driver, username, password):
        """用户名或密码为空 -> 不应登录成功。"""
        login_page = LoginPage(driver)
        login_page.login(username, password)

        assert not login_page.is_login_success(), "空输入却登录成功了"
