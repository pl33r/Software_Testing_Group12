import pytest
from unittest.mock import patch
from online_shopping_cart.product.product_search import display_filtered_table


def test_valid_csv_file_name_string(capsys):
    header = ["Product", "Price", "Quantity"]
    csv_reader = [
        ["Apple", "1.2", "10"],
        ["Banana", "0.5", "20"],
        ["Orange", "0.8", "15"]
    ]
    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        display_filtered_table(csv_file_name="products.csv", search_target=None)
        captured = capsys.readouterr()

    expected_output = "['Product', 'Price', 'Quantity']\n" \
                      "['Apple', '1.2', '10']\n" \
                      "['Banana', '0.5', '20']\n" \
                      "['Orange', '0.8', '15']"

    assert captured.out.strip() == expected_output

def test_display_filtered_table_with_valid_search(capsys):
    header = ["Product", "Price", "Quantity"]
    csv_reader = [
        ["Apple", "1.2", "10"],
        ["Banana", "0.5", "20"],
        ["Orange", "0.8", "15"]
    ]
    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        display_filtered_table(csv_file_name="products.csv", search_target="Banana")
        captured = capsys.readouterr()

    expected_output = "['Product', 'Price', 'Quantity']\n" \
                      "['Banana', '0.5', '20']"

    assert captured.out.strip() == expected_output

def test_display_filtered_table_with_empty_search(capsys):
    header = ["Product", "Price", "Quantity"]
    csv_reader = [
        ["Apple", "1.2", "10"],
        ["Banana", "0.5", "20"],
        ["Orange", "0.8", "15"]
    ]
    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        display_filtered_table(csv_file_name="products.csv", search_target="")
        captured = capsys.readouterr()

    expected_output = "['Product', 'Price', 'Quantity']"

    assert captured.out.strip() == expected_output

def test_display_filtered_table_single_product(capsys):
    header = ["Product", "Price", "Quantity"]
    csv_reader = [
        ["Apple", "1.2", "10"]
    ]
    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        display_filtered_table(csv_file_name="products.csv", search_target=None)
        captured = capsys.readouterr()

    expected_output = "['Product', 'Price', 'Quantity']\n" \
                      "['Apple', '1.2', '10']"

    assert captured.out.strip() == expected_output

def test_display_filtered_table_same_product_name(capsys):
    header = ["Product", "Price", "Quantity"]
    csv_reader = [
        ["Apple", "1.2", "10"],
        ["Apple", "0.5", "20"],
        ["Apple", "0.8", "15"]
    ]
    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        display_filtered_table(csv_file_name="products.csv", search_target="Apple")
        captured = capsys.readouterr()

    expected_output = "['Product', 'Price', 'Quantity']\n" \
                      "['Apple', '1.2', '10']\n" \
                      "['Apple', '0.5', '20']\n" \
                      "['Apple', '0.8', '15']"

    assert captured.out.strip() == expected_output

def test_display_filtered_table_special_characters(capsys):
    header = ["Product", "Price", "Quantity"]
    csv_reader = [
        ["Apple@2021", "1.2", "10"],
        ["Banana$special", "0.5", "20"],
        ["Orange&fresh", "0.8", "15"]
    ]
    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        display_filtered_table(csv_file_name="products.csv", search_target=None)
        captured = capsys.readouterr()

    expected_output = "['Product', 'Price', 'Quantity']\n" \
                      "['Apple@2021', '1.2', '10']\n" \
                      "['Banana$special', '0.5', '20']\n" \
                      "['Orange&fresh', '0.8', '15']"

    assert captured.out.strip() == expected_output


# 测试没有搜索目标时，应该显示所有的产品数据
def test_display_filtered_table_no_search_target(capsys):
    # 假设的 CSV 数据
    header = ["Product", "Price", "Quantity"]
    csv_reader = [
        ["Apple", "1.2", "10"],
        ["Banana", "0.5", "20"],
        ["Orange", "0.8", "15"]
    ]

    # 模拟 get_csv_data 返回的值
    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        # 调用 display_filtered_table，没有提供 search_target
        display_filtered_table(csv_file_name="products.csv", search_target=None)

        # 捕获输出
        captured = capsys.readouterr()

    # 预期输出包含所有产品
    expected_output = "['Product', 'Price', 'Quantity']\n" \
                      "['Apple', '1.2', '10']\n" \
                      "['Banana', '0.5', '20']\n" \
                      "['Orange', '0.8', '15']"

    assert captured.out.strip() == expected_output


# 测试提供搜索目标时，应该只显示匹配的产品
def test_display_filtered_table_with_search_target(capsys):
    # 假设的 CSV 数据
    header = ["Product", "Price", "Quantity"]
    csv_reader = [
        ["Apple", "1.2", "10"],
        ["Banana", "0.5", "20"],
        ["Orange", "0.8", "15"]
    ]

    # 模拟 get_csv_data 返回的值
    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        # 调用 display_filtered_table，搜索 "Apple"
        display_filtered_table(csv_file_name="products.csv", search_target="Apple")

        # 捕获输出
        captured = capsys.readouterr()

    # 预期输出只包含 "Apple" 产品
    expected_output = "['Product', 'Price', 'Quantity']\n" \
                      "['Apple', '1.2', '10']"

    assert captured.out.strip() == expected_output


# 测试搜索目标与任何产品都不匹配时，应该不显示任何产品
def test_display_filtered_table_no_match(capsys):
    # 假设的 CSV 数据
    header = ["Product", "Price", "Quantity"]
    csv_reader = [
        ["Apple", "1.2", "10"],
        ["Banana", "0.5", "20"],
        ["Orange", "0.8", "15"]
    ]

    # 模拟 get_csv_data 返回的值
    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        # 调用 display_filtered_table，搜索 "Pineapple"（没有匹配的产品）
        display_filtered_table(csv_file_name="products.csv", search_target="Pineapple")

        # 捕获输出
        captured = capsys.readouterr()

    # 预期输出应该只包含表头，不会有任何产品数据
    expected_output = "['Product', 'Price', 'Quantity']"

    # 通过去除尾部的换行符来比较
    # 用strip来去掉多余的空格/换行符
    assert captured.out.strip().splitlines()[0] == expected_output



# 测试大小写不敏感的匹配，应该返回匹配的产品
def test_display_filtered_table_case_insensitive(capsys):
    # 假设的 CSV 数据
    header = ["Product", "Price", "Quantity"]
    csv_reader = [
        ["Apple", "1.2", "10"],
        ["Banana", "0.5", "20"],
        ["Orange", "0.8", "15"]
    ]

    # 模拟 get_csv_data 返回的值
    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        # 调用 display_filtered_table，搜索 "apple"（忽略大小写）
        display_filtered_table(csv_file_name="products.csv", search_target="apple")

        # 捕获输出
        captured = capsys.readouterr()

    # 预期输出应该包含 "Apple" 产品（忽略大小写）
    expected_output = "['Product', 'Price', 'Quantity']\n" \
                      "['Apple', '1.2', '10']"

    assert captured.out.strip() == expected_output


    # 无效输入测试：无效的csv_file_name（整数类型）


# 无效输入测试：无效的csv_file_name（整数类型）
def test_invalid_csv_file_name_int(capsys):
    # 使用 pytest.raises 捕获 OSError 异常，使用正则表达式匹配错误信息
    with pytest.raises(OSError, match=r'.*\[WinError 6\].*'):
        display_filtered_table(csv_file_name=123, search_target=None)

# 无效输入测试：无效的csv_file_name（浮动类型）
def test_invalid_csv_file_name_float(capsys):
    # 使用 pytest.raises 捕获 TypeError 异常，使用正则表达式匹配错误信息
    with pytest.raises(TypeError, match=r'.*expected str, bytes or os.PathLike object, not float.*'):
        display_filtered_table(csv_file_name=12.34, search_target=None)


def test_invalid_csv_file_name_list(capsys):
    # 使用 pytest.raises 捕获 TypeError 异常，使用正则表达式匹配错误信息
    with pytest.raises(TypeError, match=r'.*expected str, bytes or os.PathLike object, not list.*'):
        display_filtered_table(csv_file_name=['invalid', 'list'], search_target=None)


def test_invalid_csv_file_name_string(capsys):
    # 模拟一个无效的文件路径，应该抛出 FileNotFoundError
    with pytest.raises(FileNotFoundError, match=r'.*No such file or directory.*'):
        display_filtered_table(csv_file_name="invalid_path.csv", search_target=None)
