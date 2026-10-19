from api.request_client import send_request


# BASE_URL = "http://127.0.0.1:8015"

# 商品列表接口地址
# PRODUCTS_URL = f"{BASE_URL}/products"
# 商品接口基础路径
PRODUCTS_PATH = "/products"



def get_products():
    """获取商品列表并返回完整响应"""
    response = send_request(
        method="get",
        path=PRODUCTS_PATH
    )
    return response

def get_product_detail(product_id):
    """根据商品ID获取商品详情并返回完整响应"""
    # product_id属于Path参数 由API层负责拼接接口地址
    product_detail_path = f"{PRODUCTS_PATH}/{product_id}"

    response = send_request(
        method="get",
        path=product_detail_path
    )

    return response