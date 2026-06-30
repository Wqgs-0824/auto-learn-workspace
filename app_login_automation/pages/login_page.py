"""登录页面对象（Page Object）。

元素定位器只是示例，请用 Appium Inspector 查看被测 APP 后替换为真实的
resource-id / xpath / accessibility id。
"""
from appium.webdriver.common.appiumby import AppiumBy

from .base_page import BasePage


class LoginPage(BasePage):
    """登录页：封装用户名/密码输入、登录按钮点击、结果校验。"""

    # ---- 元素定位器（按实际 APP 修改）----
    USERNAME_INPUT = (AppiumBy.ID, "com.example.demo:id/et_username")
    PASSWORD_INPUT = (AppiumBy.ID, "com.example.demo:id/et_password")
    LOGIN_BUTTON = (AppiumBy.ID, "com.example.demo:id/btn_login")
    # 登录成功后才会出现的元素（如首页的“我的”入口）
    HOME_FLAG = (AppiumBy.ID, "com.example.demo:id/tab_mine")
    # 登录失败时弹出的错误提示
    ERROR_TOAST = (
        AppiumBy.XPATH,
        '//android.widget.Toast[contains(@text, "用户名或密码错误")]',
    )

    # ---- 页面操作 ----
    def input_username(self, username):
        self.input_text(self.USERNAME_INPUT, username)
        return self

    def input_password(self, password):
        self.input_text(self.PASSWORD_INPUT, password)
        return self

    def tap_login(self):
        self.click(self.LOGIN_BUTTON)
        return self

    def login(self, username, password):
        """完整登录流程。"""
        self.input_username(username)
        self.input_password(password)
        self.tap_login()
        return self

    # ---- 结果校验 ----
    def is_login_success(self):
        """通过首页特征元素判断是否登录成功。"""
        return self.is_displayed(self.HOME_FLAG, timeout=10)

    def is_error_shown(self):
        """判断是否出现登录失败提示（Toast 一闪而过，超时时间设短一些）。"""
        return self.is_displayed(self.ERROR_TOAST, timeout=5)
