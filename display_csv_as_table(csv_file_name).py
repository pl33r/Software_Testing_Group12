import pytest
from unittest.mock import patch, mock_open
from online_shopping_cart.product.product_search import display_csv_as_table


# 测试无效输入：负数
def test_display_csv_as_table_negative_number(capsys):
    """
    测试输入的数量为负数的情况。
    """
    negative_number_csv = "Product,Price,Quantity\nApple,1.2,-10"

    # 模拟 get_csv_data 的返回值
    header = ["Product", "Price", "Quantity"]
    csv_reader = [["Apple", "1.2", "-10"]]  # 负数作为数量

    # 预期输出（列表格式字符串）
    expected_output = (
        "['Product', 'Price', 'Quantity']\n"
        "['Apple', '1.2', '-10']"
    )

    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        with patch("builtins.open", mock_open(read_data=negative_number_csv)):
            display_csv_as_table("negative_number.csv")
            captured = capsys.readouterr()
            assert captured.out.strip() == expected_output


# 测试无效输入：空字符串作为文件名
def test_display_csv_as_table_empty_string(capsys):
    """
    测试文件名为空字符串的情况。
    """
    empty_string_csv = ""  # 空字符串作为文件名

    with pytest.raises(Exception):  # 应该抛出异常
        display_csv_as_table(csv_file_name=empty_string_csv)


# 测试无效输入：文件名为数字
def test_display_csv_as_table_numeric_file_name(capsys):
    """
    测试文件名为数字的情况。
    """
    numeric_file_name = "12345"  # 数字作为文件名

    with pytest.raises(OSError):  # 应该抛出文件打开错误
        display_csv_as_table(csv_file_name=numeric_file_name)


# 测试无效输入：无效类型
@pytest.mark.parametrize("invalid_input", [123, 45.67, ["list"], None])
def test_display_csv_as_table_invalid_input(invalid_input):
    """
    测试无效输入类型：int, float, list, None。
    确保函数抛出 OSError 或其他合理错误。
    """
    with pytest.raises(Exception) as excinfo:  # 捕获所有异常，验证函数行为
        display_csv_as_table(csv_file_name=invalid_input)

    # 检查抛出的异常类型是否合理
    assert isinstance(excinfo.value, (TypeError, OSError, ValueError)), \
        f"Unexpected exception type: {type(excinfo.value)}"


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
