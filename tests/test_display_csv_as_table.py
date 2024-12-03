import pytest
from unittest.mock import patch, mock_open
from online_shopping_cart.product.product_search import display_csv_as_table


# Test invalid input: Integer as file name
def test_display_csv_as_table_invalid_input_int():
    """Test invalid input: Integer as file name"""
    invalid_input = 123  # An integer instead of a string
    with pytest.raises(OSError) as excinfo:
        display_csv_as_table(csv_file_name=invalid_input)
    assert isinstance(excinfo.value, OSError)


# Test invalid input: Float as file name
def test_display_csv_as_table_invalid_input_float():
    """Test invalid input: Float as file name"""
    invalid_input = 45.67  # A float instead of a string
    with pytest.raises(TypeError, match="expected str, bytes or os.PathLike object, not float") as excinfo:
        display_csv_as_table(csv_file_name=invalid_input)
    assert isinstance(excinfo.value, TypeError)

# Test invalid input: List as file name
def test_display_csv_as_table_invalid_input_list():
    """Test invalid input: List as file name"""
    invalid_input = ["file1.csv", "file2.csv"]  # A list instead of a string
    with pytest.raises(TypeError, match="expected str, bytes or os.PathLike object, not list") as excinfo:
        display_csv_as_table(csv_file_name=invalid_input)
    assert isinstance(excinfo.value, TypeError)

def test_display_csv_as_table_invalid_input_none():
    """Test invalid input: None as file name"""
    invalid_input = None  # None 输入
    with pytest.raises(TypeError) as excinfo:
        display_csv_as_table(csv_file_name=invalid_input)
    #
    assert str(excinfo.value) == "File name must be a string"



#2 Test invalid input: None as file name
# def test_display_csv_as_table_invalid_input_none():
#     """Test invalid input: None as file name"""
#     invalid_input = None  # None instead of a string
#     # We simulate the behavior of raising TypeError with a specific message.
#     with pytest.raises(TypeError, match="expected str, bytes or os.PathLike object, not NoneType") as excinfo:
#         display_csv_as_table(csv_file_name=invalid_input)
#     assert isinstance(excinfo.value, TypeError)
#     # Ensure the exception message matches the Python built-in error message
#     assert str(excinfo.value) == "expected str, bytes or os.PathLike object, not NoneType"


#3 # Test invalid input: None as file name
# def test_display_csv_as_table_invalid_input_none():
#     """Test invalid input: None as file name"""
#     invalid_input = None  # None instead of a string
#
#     # Manually capture exceptions and verify exception information
#     try:
#         display_csv_as_table(csv_file_name=invalid_input)
#     except TypeError as e:
#         # capture the exception and verify
#         assert str(e) == "expected str, bytes or os.PathLike object, not NoneType"
#     else:
#         # if not be captuerd, test failed
#         pytest.fail("TypeError was not raised for None input")



# Test for the case when the file does not exist
def test_display_csv_as_table_file_not_found():
    """Test for the case when the file is not found, ensuring the function handles FileNotFoundError correctly."""
    with pytest.raises(FileNotFoundError):
        display_csv_as_table("non_existent_file.csv")


# Test for the case when the file is empty
def test_display_csv_as_table_empty_file():
    """Test for the case when the file is empty, ensuring the function throws an exception or returns empty table info."""
    with patch("builtins.open", mock_open(read_data="")):
        with pytest.raises(StopIteration):
            display_csv_as_table("empty_file.csv")

# # Test for the case when the file is not a valid CSV
# def test_display_csv_as_table_invalid_file():
#     """Test for an invalid file path input, ensuring an OSError or FileNotFoundError is raised."""
#     invalid_file = "invalid_file.csv"  # Assuming the file does not exist
#     with pytest.raises(OSError):  # Could also be FileNotFoundError, depending on the file opening behavior
#         display_csv_as_table(csv_file_name=invalid_file)

def test_display_csv_as_table_invalid_file(capsys):
    """Test for an invalid file path input, ensuring an OSError or FileNotFoundError is raised."""
    invalid_file = "invalid_file.csv"  # Assuming the file does not exist

    # Define the expected behavior (e.g., exception raised)
    expected_exception = OSError
    expected_message = "No such file or directory"

    try:
        display_csv_as_table(csv_file_name=invalid_file)
    except expected_exception as exc:
        # Capture the output from the exception and validate it
        actual_message = str(exc)

        # Assert the exception message
        assert expected_message in actual_message, f"Expected: {expected_message}, but got: {actual_message}"

        # Print expected and actual for debugging
        print(f"Expected exception message: {expected_message}")
        print(f"Actual exception message: {actual_message}")
    else:
        pytest.fail(f"Expected {expected_exception.__name__} was not raised.")

    # Optionally, check if any output was captured and print it
    captured = capsys.readouterr()
    print("Captured standard output:", captured.out)
    print("Captured standard error:", captured.err)


# Test case when the CSV file only has header row
def test_display_csv_as_table_header_only(capsys):
    """Test the case when the file contains only the header row."""
    header_only_csv = "Product,Price,Quantity\n"

    # Simulate the return value of get_csv_data
    header = ["Product", "Price", "Quantity"]
    csv_reader = []  # Empty data rows

    # Expected output should be a string representation of a list
    expected_output = "['Product', 'Price', 'Quantity']"

    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        with patch("builtins.open", mock_open(read_data=header_only_csv)):
            display_csv_as_table("header_only.csv")
            captured = capsys.readouterr()
            assert captured.out.strip() == expected_output

# Test case when the CSV file contains only one data row
def test_display_csv_as_table_single_row(capsys):
    """Test the case when the file contains only one data row."""
    single_row_csv = "Product,Price,Quantity\nApple,1.2,10"

    # Simulate the return value of get_csv_data
    header = ["Product", "Price", "Quantity"]
    csv_reader = [["Apple", "1.2", "10"]]

    # Expected output should be a string representation of a list
    expected_output = (
        "['Product', 'Price', 'Quantity']\n"
        "['Apple', '1.2', '10']"
    )

    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        with patch("builtins.open", mock_open(read_data=single_row_csv)):
            display_csv_as_table("single_row.csv")
            captured = capsys.readouterr()
            assert captured.out.strip() == expected_output

# Test case when the CSV file contains multiple data rows
def test_display_csv_as_table_multiple_rows(capsys):
    """Test the case when the file contains multiple data rows."""
    multiple_rows_csv = "Product,Price,Quantity\nApple,1.2,10\nBanana,0.5,20\nOrange,0.8,15"

    # Simulate the return value of get_csv_data
    header = ["Product", "Price", "Quantity"]
    csv_reader = [["Apple", "1.2", "10"], ["Banana", "0.5", "20"], ["Orange", "0.8", "15"]]

    # Expected output (string representation of a list)
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

# Test case when the CSV file contains various data types (strings and numbers)
def test_display_csv_as_table_various_data_types(capsys):
    """Test the case when the file contains various data types (strings and numbers)."""
    various_data_csv = "Product,Price,Quantity\nApple,1.2,10\nOrange,0.8,15"

    # Simulate the return value of get_csv_data
    header = ["Product", "Price", "Quantity"]
    csv_reader = [["Apple", "1.2", "10"], ["Orange", "0.8", "15"]]

    # Expected output (string representation of a list)
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

# Test case when the product name contains special characters (e.g., comma)
def test_display_csv_as_table_special_characters(capsys):
    """Test the case when the product name contains special characters (such as a comma)."""
    special_characters_csv = "Product,Price,Quantity\nApple,1.2,10\nBanana-Special,0.5,20"

    # Simulate the return value of get_csv_data
    header = ["Product", "Price", "Quantity"]
    csv_reader = [["Apple", "1.2", "10"], ["Banana-Special", "0.5", "20"]]

    # Expected output (string representation of a list)
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

# Test case when the product name contains spaces
def test_display_csv_as_table_product_with_spaces(capsys):
    """Test the case when the product name contains spaces."""
    product_with_spaces_csv = "Product,Price,Quantity\nApple Juice,1.2,10"

    # Simulate the return value of get_csv_data
    header = ["Product", "Price", "Quantity"]
    csv_reader = [["Apple Juice", "1.2", "10"]]

    # Expected output (string representation of a list)
    expected_output = (
        "['Product', 'Price', 'Quantity']\n"
        "['Apple Juice', '1.2', '10']"
    )

    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        with patch("builtins.open", mock_open(read_data=product_with_spaces_csv)):
            display_csv_as_table("product_with_spaces.csv")
            captured = capsys.readouterr()
            assert captured.out.strip() == expected_output

# Test case when the product price is an integer
def test_display_csv_as_table_product_price_integer(capsys):
    """Test the case when the product price is an integer."""
    product_price_integer_csv = "Product,Price,Quantity\nApple,10,20"

    # Simulate the return value of get_csv_data
    header = ["Product", "Price", "Quantity"]
    csv_reader = [["Apple", "10", "20"]]

    # Expected output (string representation of a list)
    expected_output = (
        "['Product', 'Price', 'Quantity']\n"
        "['Apple', '10', '20']"
    )

    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        with patch("builtins.open", mock_open(read_data=product_price_integer_csv)):
            display_csv_as_table("product_price_integer.csv")
            captured = capsys.readouterr()
            assert captured.out.strip() == expected_output

# Test case when the product price is a floating point number
def test_display_csv_as_table_product_price_float(capsys):
    """Test the case when the product price is a floating point number."""
    product_price_float_csv = "Product,Price,Quantity\nApple,1.50,10"

    # Simulate the return value of get_csv_data
    header = ["Product", "Price", "Quantity"]
    csv_reader = [["Apple", "1.50", "10"]]

    # Expected output (string representation of a list)
    expected_output = (
        "['Product', 'Price', 'Quantity']\n"
        "['Apple', '1.50', '10']"
    )

    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        with patch("builtins.open", mock_open(read_data=product_price_float_csv)):
            display_csv_as_table("product_price_float.csv")
            captured = capsys.readouterr()
            assert captured.out.strip() == expected_output

# Test case when the CSV file contains large numbers
def test_display_csv_as_table_large_numbers(capsys):
    """Test the case when the file contains large numbers."""
    large_numbers_csv = "Product,Price,Quantity\nBigProduct,10000,5000"

    # Simulate the return value of get_csv_data
    header = ["Product", "Price", "Quantity"]
    csv_reader = [["BigProduct", "10000", "5000"]]

    # Expected output (string representation of a list)
    expected_output = (
        "['Product', 'Price', 'Quantity']\n"
        "['BigProduct', '10000', '5000']"
    )

    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        with patch("builtins.open", mock_open(read_data=large_numbers_csv)):
            display_csv_as_table("large_numbers.csv")
            captured = capsys.readouterr()
            assert captured.out.strip() == expected_output

# Test case when the product name is empty
def test_display_csv_as_table_empty_product_name(capsys):
    """Test the case when the product name is empty."""
    empty_product_name_csv = "Product,Price,Quantity\n,10,5"

    # Simulate the return value of get_csv_data
    header = ["Product", "Price", "Quantity"]
    csv_reader = [["", "10", "5"]]

    # Expected output (string representation of a list)
    expected_output = (
        "['Product', 'Price', 'Quantity']\n"
        "['', '10', '5']"
    )

    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        with patch("builtins.open", mock_open(read_data=empty_product_name_csv)):
            display_csv_as_table("empty_product_name.csv")
            captured = capsys.readouterr()
            assert captured.out.strip() == expected_output
