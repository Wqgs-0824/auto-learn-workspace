import os

# 接口基础地址
BASE_URL = "http://127.0.0.1:8015"

# 优先读取环境变量 未设置时使用本地服务地址
BASE_URL = os.getenv(
    "MICROSHOP_BASE_URL",
    BASE_URL
)

# 公共请求层的默认超时 单位：秒
DEFAULT_TIMEOUT = float(
    os.getenv(
        "MICROSHOP_TIMEOUT",
        "5"
    )
)

# 默认超时必须大于0
if DEFAULT_TIMEOUT <= 0:
    raise ValueError("MICROSHOP_TIMEOUT 必须大于0")

