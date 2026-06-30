"""页面对象基类：封装常用的元素查找、点击、输入等操作，带显式等待。"""
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """所有 Page Object 的基类。"""

    # 默认显式等待时间（秒）
    DEFAULT_TIMEOUT = 15

    def __init__(self, driver):
        self.driver = driver

    def _wait(self, timeout=None):
        return WebDriverWait(self.driver, timeout or self.DEFAULT_TIMEOUT)

    def find(self, locator, timeout=None):
        """等待元素出现并返回该元素。locator 形如 (AppiumBy.ID, "xxx")。"""
        return self._wait(timeout).until(EC.presence_of_element_located(locator))

    def click(self, locator, timeout=None):
        """等待元素可点击后点击。"""
        self._wait(timeout).until(EC.element_to_be_clickable(locator)).click()

    def input_text(self, locator, text, timeout=None):
        """清空输入框后输入文本。"""
        element = self.find(locator, timeout)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator, timeout=None):
        """获取元素文本。"""
        return self.find(locator, timeout).text

    def is_displayed(self, locator, timeout=5):
        """判断元素是否在指定时间内出现，未出现返回 False（不抛异常）。"""
        try:
            self.find(locator, timeout)
            return True
        except Exception:
            return False
