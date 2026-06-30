# APP 端登录 UI 自动化

基于 **Appium + Python + pytest**，采用 **Page Object Model（POM）** 设计的移动 APP 登录自动化脚本。默认针对 Android，稍作修改即可用于 iOS。

## 目录结构

```
app_login_automation/
├── config/
│   └── caps.yaml            # Appium 启动参数 + 测试账号
├── pages/
│   ├── base_page.py         # 页面基类：封装等待、点击、输入
│   └── login_page.py        # 登录页对象：元素定位 + 业务操作
├── tests/
│   ├── conftest.py          # pytest fixture：启动/退出 driver
│   └── test_login.py        # 登录测试用例
├── utils/
│   └── config_loader.py     # 读取 YAML 配置
├── pytest.ini               # pytest 配置
├── requirements.txt         # 依赖
└── report/                  # HTML 测试报告输出目录
```

## 环境准备

1. **JDK 8+** 与 **Android SDK**（配好 `adb` 环境变量）。
2. **Node.js**，并安装 Appium 2 与驱动：
   ```bash
   npm install -g appium
   appium driver install uiautomator2
   ```
3. **Python 3.8+**，安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
4. 连接真机（开启 USB 调试）或启动 Android 模拟器，确认 `adb devices` 能看到设备。

## 使用步骤

1. 修改 `config/caps.yaml`：
   - `appPackage` / `appActivity`：被测 APP 的包名与登录页 Activity
     （获取：`adb shell dumpsys window | grep mCurrentFocus`）。
   - `deviceName` / `platformVersion`：你的设备信息。
   - `account`：有效与无效的测试账号。
2. 修改 `pages/login_page.py` 中的**元素定位器**（用户名框、密码框、登录按钮、
   登录成功标志、错误提示），用 **Appium Inspector** 查看真实的 `resource-id`/`xpath`。
3. 启动 Appium Server：
   ```bash
   appium
   ```
4. 运行测试：
   ```bash
   # 全部用例
   pytest

   # 只跑登录成功用例
   pytest tests/test_login.py::TestLogin::test_login_success
   ```
5. 测试报告生成在 `report/report.html`。

## 包含的测试用例

| 用例 | 说明 |
| --- | --- |
| `test_login_success` | 正确账号密码 → 登录成功，进入首页 |
| `test_login_wrong_password` | 密码错误 → 出现错误提示，未登录 |
| `test_login_empty_input` | 用户名/密码为空（参数化）→ 不应登录成功 |

## 改造为 iOS

- `caps.yaml` 中 `platformName` 改为 `iOS`，`automationName` 改为 `XCUITest`，
  并配置 `bundleId` 等。
- `conftest.py` 改用 `appium.options.ios.XCUITestOptions`。
- `login_page.py` 的定位器改用 iOS 的 `accessibility id` / `-ios predicate string`。
