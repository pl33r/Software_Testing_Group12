import pytest
from unittest.mock import patch, mock_open
from online_shopping_cart.product.product_search import display_csv_as_table


def test_display_csv_as_table_invalid_input_int():
    """Test invalid input: Integer as file name"""
    invalid_input = 123  # An integer instead of a string
    with pytest.raises(TypeError, match="File name must be a string") as excinfo:
        display_csv_as_table(csv_file_name=invalid_input)
    assert isinstance(excinfo.value, TypeError)



def test_display_csv_as_table_invalid_input_float():
    """Test invalid input: Float as file name"""
    invalid_input = 45.67  # A float instead of a string
    with pytest.raises(TypeError, match="File name must be a string") as excinfo:
        display_csv_as_table(csv_file_name=invalid_input)
    assert isinstance(excinfo.value, TypeError)
def test_display_csv_as_table_invalid_input_list():
    """Test invalid input: List as file name"""
    invalid_input = ["file1.csv", "file2.csv"]  # A list instead of a string
    with pytest.raises(TypeError, match="File name must be a string") as excinfo:
        display_csv_as_table(csv_file_name=invalid_input)
    assert isinstance(excinfo.value, TypeError)
def test_display_csv_as_table_invalid_input_none():
    """Test invalid input: None as file name"""
    invalid_input = None  # None instead of a string
    with pytest.raises(TypeError, match="File name must be a string") as excinfo:
        display_csv_as_table(csv_file_name=invalid_input)
    assert isinstance(excinfo.value, TypeError)


# 测试文件不存在的情况
def test_display_csv_as_table_file_not_found():
    """
    测试文件不存在时，函数是否正确处理 FileNotFoundError。
    """
    with pytest.raises(FileNotFoundError):
        display_csv_as_table("non_existent_file.csv")


# 测试文件为空的情况
def test_display_csv_as_table_empty_file():
    """
    测试文件为空时，函数是否正确抛出异常或返回空表信息。
    """
    with patch("builtins.open", mock_open(read_data="")):
        with pytest.raises(StopIteration):
            display_csv_as_table("empty_file.csv")


# 测试文件不是合法 CSV 格式时
def test_display_csv_as_table_invalid_file():
    """
    测试无效文件路径输入，确保抛出 OSError 或 FileNotFoundError。
    """
    invalid_file = "invalid_file.csv"  # 假设文件不存在
    with pytest.raises(OSError):  # 也可以是 FileNotFoundError，取决于文件打开的行为
        display_csv_as_table(csv_file_name=invalid_file)


# 以下为有效输入测试用例

# 测试有效的CSV文件（只有标题行）
def test_display_csv_as_table_header_only(capsys):
    """
    测试文件只有标题行的情况。
    """
    header_only_csv = "Product,Price,Quantity\n"

    # 模拟 get_csv_data 的返回值
    header = ["Product", "Price", "Quantity"]
    csv_reader = []  # 空数据行

    # 预期输出应该是一个类似列表的字符串形式
    expected_output = "['Product', 'Price', 'Quantity']"

    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        with patch("builtins.open", mock_open(read_data=header_only_csv)):
            display_csv_as_table("header_only.csv")
            captured = capsys.readouterr()
            assert captured.out.strip() == expected_output


# 测试有效的CSV文件（只有一行数据）
def test_display_csv_as_table_single_row(capsys):
    """
    测试文件只有一行数据的情况。
    """
    single_row_csv = "Product,Price,Quantity\nApple,1.2,10"

    # 模拟 get_csv_data 的返回值
    header = ["Product", "Price", "Quantity"]
    csv_reader = [["Apple", "1.2", "10"]]

    # 预期输出应该是类似列表的字符串形式
    expected_output = (
        "['Product', 'Price', 'Quantity']\n"
        "['Apple', '1.2', '10']"
    )

    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        with patch("builtins.open", mock_open(read_data=single_row_csv)):
            display_csv_as_table("single_row.csv")
            captured = capsys.readouterr()
            assert captured.out.strip() == expected_output


# 测试有效的CSV文件（包含多行数据）
def test_display_csv_as_table_multiple_rows(capsys):
    """
    测试文件包含多行数据的情况。
    """
    multiple_rows_csv = "Product,Price,Quantity\nApple,1.2,10\nBanana,0.5,20\nOrange,0.8,15"

    # 模拟 get_csv_data 的返回值
    header = ["Product", "Price", "Quantity"]
    csv_reader = [["Apple", "1.2", "10"], ["Banana", "0.5", "20"], ["Orange", "0.8", "15"]]

    # 预期输出（列表格式字符串）
    expected_output = (
        "['Product', 'Price', 'Quantity']\n"
        "['Apple', '1.2', '10']\n"
        "['Banana', '0.5', '20']\n"
        "['Orange', '0.8', '15']"
    )

    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        with patch("builtins.open", mock_open(read_data=multiple_rows_csv)):
            display_csv_as_table("multiple_rows.csv")
            captured = capsys.readouterr()
            assert captured.out.strip() == expected_output


# 测试有效的输入：文件包含不同数据类型（字符串、数字）
def test_display_csv_as_table_various_data_types(capsys):
    """
    测试文件包含多种数据类型（字符串和数字）的情况。
    """
    various_data_csv = "Product,Price,Quantity\nApple,1.2,10\nOrange,0.8,15"

    # 模拟 get_csv_data 的返回值
    header = ["Product", "Price", "Quantity"]
    csv_reader = [["Apple", "1.2", "10"], ["Orange", "0.8", "15"]]

    # 预期输出（列表格式字符串）
    expected_output = (
        "['Product', 'Price', 'Quantity']\n"
        "['Apple', '1.2', '10']\n"
        "['Orange', '0.8', '15']"
    )

    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        with patch("builtins.open", mock_open(read_data=various_data_csv)):
            display_csv_as_table("various_data.csv")
            captured = capsys.readouterr()
            assert captured.out.strip() == expected_output


# 测试有效的输入：商品名包含特殊字符（如逗号）
def test_display_csv_as_table_special_characters(capsys):
    """
    测试文件中商品名包含特殊字符的情况。
    """
    special_characters_csv = "Product,Price,Quantity\nApple,1.2,10\nBanana-Special,0.5,20"

    # 模拟 get_csv_data 的返回值
    header = ["Product", "Price", "Quantity"]
    csv_reader = [["Apple", "1.2", "10"], ["Banana-Special", "0.5", "20"]]

    # 预期输出（列表格式字符串）
    expected_output = (
        "['Product', 'Price', 'Quantity']\n"
        "['Apple', '1.2', '10']\n"
        "['Banana-Special', '0.5', '20']"
    )

    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        with patch("builtins.open", mock_open(read_data=special_characters_csv)):
            display_csv_as_table("special_characters.csv")
            captured = capsys.readouterr()
            assert captured.out.strip() == expected_output

# 测试有效的CSV文件（商品名中包含空格）
def test_display_csv_as_table_product_with_spaces(capsys):
    """
    测试商品名包含空格的情况。
    """
    product_with_spaces_csv = "Product,Price,Quantity\nApple Juice,1.2,10"

    # 模拟 get_csv_data 的返回值
    header = ["Product", "Price", "Quantity"]
    csv_reader = [["Apple Juice", "1.2", "10"]]

    # 预期输出（列表格式字符串）
    expected_output = (
        "['Product', 'Price', 'Quantity']\n"
        "['Apple Juice', '1.2', '10']"
    )

    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        with patch("builtins.open", mock_open(read_data=product_with_spaces_csv)):
            display_csv_as_table("product_with_spaces.csv")
            captured = capsys.readouterr()
            assert captured.out.strip() == expected_output


# 测试有效的CSV文件（商品价格为整数）
def test_display_csv_as_table_product_price_integer(capsys):
    """
    测试商品价格为整数的情况。
    """
    product_price_integer_csv = "Product,Price,Quantity\nApple,10,20"

    # 模拟 get_csv_data 的返回值
    header = ["Product", "Price", "Quantity"]
    csv_reader = [["Apple", "10", "20"]]

    # 预期输出（列表格式字符串）
    expected_output = (
        "['Product', 'Price', 'Quantity']\n"
        "['Apple', '10', '20']"
    )

    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        with patch("builtins.open", mock_open(read_data=product_price_integer_csv)):
            display_csv_as_table("product_price_integer.csv")
            captured = capsys.readouterr()
            assert captured.out.strip() == expected_output


# 测试有效的CSV文件（商品价格为浮动小数）
def test_display_csv_as_table_product_price_float(capsys):
    """
    测试商品价格为浮动的小数类型的情况。
    """
    product_price_float_csv = "Product,Price,Quantity\nApple,1.50,10"

    # 模拟 get_csv_data 的返回值
    header = ["Product", "Price", "Quantity"]
    csv_reader = [["Apple", "1.50", "10"]]

    # 预期输出（列表格式字符串）
    expected_output = (
        "['Product', 'Price', 'Quantity']\n"
        "['Apple', '1.50', '10']"
    )

    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        with patch("builtins.open", mock_open(read_data=product_price_float_csv)):
            display_csv_as_table("product_price_float.csv")
            captured = capsys.readouterr()
            assert captured.out.strip() == expected_output


# 测试有效的CSV文件（包含大数值）
def test_display_csv_as_table_large_numbers(capsys):
    """
    测试文件包含大数值的情况。
    """
    large_numbers_csv = "Product,Price,Quantity\nBigProduct,10000,5000"

    # 模拟 get_csv_data 的返回值
    header = ["Product", "Price", "Quantity"]
    csv_reader = [["BigProduct", "10000", "5000"]]

    # 预期输出（列表格式字符串）
    expected_output = (
        "['Product', 'Price', 'Quantity']\n"
        "['BigProduct', '10000', '5000']"
    )

    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        with patch("builtins.open", mock_open(read_data=large_numbers_csv)):
            display_csv_as_table("large_numbers.csv")
            captured = capsys.readouterr()
            assert captured.out.strip() == expected_output


# 测试有效的CSV文件（商品名为空）
def test_display_csv_as_table_empty_product_name(capsys):
    """
    测试商品名为空的情况。
    """
    empty_product_name_csv = "Product,Price,Quantity\n,10,5"

    # 模拟 get_csv_data 的返回值
    header = ["Product", "Price", "Quantity"]
    csv_reader = [["", "10", "5"]]

    # 预期输出（列表格式字符串）
    expected_output = (
        "['Product', 'Price', 'Quantity']\n"
        "['', '10', '5']"
    )

    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        with patch("builtins.open", mock_open(read_data=empty_product_name_csv)):
            display_csv_as_table("empty_product_name.csv")
            captured = capsys.readouterr()
            assert captured.out.strip() == expected_output