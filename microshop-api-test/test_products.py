from api.products_api import (
    get_products,
    get_product_detail
)

# import requests

# BASE_URL = "http://127.0.0.1:8015"


def test_get_products_lists():
    products_response = get_products()

    # 测试层继续验证http状态码
    assert products_response.status_code == 200

    # 测试层解析json响应体
    products_body = products_response.json()

    # 断言响应数据是列表
    assert isinstance(products_body, list)
    # 断言商品列表不为空
    assert len(products_body) > 0
    # 取出第一件商品
    first_product = products_body[0]

    # {...} 创建一个集合，适合保存不重复的必需字段。
    # first_product.keys() 获取商品字典的所有键。
    # issubset() 检查左侧集合的每个字段是否都存在于右侧集合中。
    required_fields = {"id", "name", "price", "stock", "is_active"}
    assert required_fields.issubset(first_product.keys())

def test_get_product_detail_success():
    """验证从商品列表提取真实 ID 后能获取同一件商品的详情。"""
    products_list_response = get_products()

    assert products_list_response.status_code == 200

    products_list_body = products_list_response.json()

    # 确保存在可用于下游详情请求的商品
    assert products_list_body

    # 从上游商品列表中提取第一件商品的真实 ID
    product_id = products_list_body[0]["id"]

    # 将上游返回的 ID 放入下游商品详情接口的 Path
    # product_detail_url = f"{BASE_URL}/products/{product_id}"
    product_detail_response = get_product_detail(product_id)
    assert product_detail_response.status_code == 200

    product_detail_body = product_detail_response.json()

    # 验证详情接口返回的是列表中选中的同一件商品
    assert product_detail_body["id"] == product_id

    # 验证商品详情包含必要字段
    required_fields = {"id", "name", "price", "stock", "is_active"}
    assert required_fields.issubset(product_detail_body.keys())

def test_get_nonexistent_product_returns_404():
    """验证查询不存在的商品时返回 404 和业务错误信息。"""

    # 测试层负责准备当前异常场景的数据
    nonexistent_product_id = 99999

    # API层负责拼接path并发送商品详情请求
    product_error_response = get_product_detail(nonexistent_product_id)

    # 测试层验证本场景期望的404场景
    assert product_error_response.status_code == 404

    product_error_response_body = product_error_response.json()

    # 断言detail=商品不存在
    assert product_error_response_body["detail"] == "商品不存在"

