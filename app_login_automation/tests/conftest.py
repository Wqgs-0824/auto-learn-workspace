"""pytest 公共 fixture：初始化 / 释放 Appium driver。"""
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

from utils.config_loader import load_config


@pytest.fixture(scope="session")
def config():
    """加载一次配置，整个测试会话共享。"""
    return load_config()


@pytest.fixture
def driver(config):
    """每个测试用例启动一个全新的 Appium 会话，结束后退出。"""
    options = UiAutomator2Options().load_capabilities(config["capabilities"])
    drv = webdriver.Remote(config["server_url"], options=options)
    drv.implicitly_wait(5)
    yield drv
    drv.quit()
