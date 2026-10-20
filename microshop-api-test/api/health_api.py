from api.request_client import send_request

# 健康检查接口路径
HEALTH_PATH = "/health"

def get_health():
    """查询服务健康状态，并返回完整响应"""
    response = send_request(
        method="get",
        path=HEALTH_PATH
    )
    return response