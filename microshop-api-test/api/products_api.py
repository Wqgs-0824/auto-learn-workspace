import requests

BASE_URL = "http://127.0.0.1:8015"

# 商品列表接口地址
PRODUCTS_URL = f"{BASE_URL}/products"

def get_products():
    """获取商品列表并返回完整响应"""
    response = requests.get(
        url=PRODUCTS_URL
    )

    return response

def get_product_detail(product_id):
    """根据商品ID获取商品详情并返回完整响应"""
    # product_id属于Path参数 由API层负责拼接接口地址
    product_detail_url = f"{PRODUCTS_URL}/{product_id}"

    response = requests.get(
        url=product_detail_url
    )

    return response