import pytest
from unittest.mock import patch
from online_shopping_cart.product.product import Product
from online_shopping_cart.user.user_interface import UserInterface

# 创建一个模拟的产品数据
mock_product_data = [
    Product(name="Laptop", price=1000.00, units=5),
    Product(name="Phone", price=500.00, units=10),
]

# 模拟用户数据
mock_user_data = [{'username': 'testuser', 'password': 'testpassword'}]

# 测试 - 查询所有商品
def test_search_input_all():
    with patch.object(UserInterface, 'get_user_input', side_effect=['all', 'y']):  # 返回用户输入的 'all'
        with patch('online_shopping_cart.product.product_data.get_csv_data',
                   return_value=(
                       ['Product', 'Price', 'Units'],  # 返回符合预期格式的 header
                       [
                           {'Product': 'Laptop', 'Price': 1000.0, 'Units': 5},
                           {'Product': 'Phone', 'Price': 500.0, 'Units': 10}
                       ])):  # 返回字典格式的 csv 数据
            with patch('online_shopping_cart.product.product_search.display_csv_as_table') as mock_display_all:
                with patch('online_shopping_cart.product.product_data.get_products', return_value=mock_product_data):
                    with patch('online_shopping_cart.user.user_login.login', return_value={'username': 'testuser', 'password': 'testpassword'}):
                        with patch('online_shopping_cart.user.user_data.UserDataManager.load_users', return_value=mock_user_data):
                            with patch('online_shopping_cart.checkout.checkout_process.checkout_and_payment') as mock_checkout:
                                from online_shopping_cart.shop.shop_search_and_purchase import search_and_purchase_product
                                search_and_purchase_product()  # 执行查询操作

                mock_display_all.assert_called_once()  # 确保查询所有商品的函数被调用
                mock_checkout.assert_called_once()  # 确保结账函数被调用





