import pytest
from unittest.mock import patch
from online_shopping_cart.product.product_search import display_filtered_table


def test_valid_csv_file_name_string(capsys):
    # Sample CSV data with headers and some products
    header = ["Product", "Price", "Quantity"]
    csv_reader = [
        ["Apple", "1.2", "10"],
        ["Banana", "0.5", "20"],
        ["Orange", "0.8", "15"]
    ]
    # Mocking get_csv_data to return our sample data
    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        display_filtered_table(csv_file_name="products.csv", search_target=None)
        captured = capsys.readouterr()

    expected_output = "['Product', 'Price', 'Quantity']\n" \
                      "['Apple', '1.2', '10']\n" \
                      "['Banana', '0.5', '20']\n" \
                      "['Orange', '0.8', '15']"

    assert captured.out.strip() == expected_output

def test_display_filtered_table_with_valid_search(capsys):
    # Sample CSV data with headers and some products
    header = ["Product", "Price", "Quantity"]
    csv_reader = [
        ["Apple", "1.2", "10"],
        ["Banana", "0.5", "20"],
        ["Orange", "0.8", "15"]
    ]
    # Mocking get_csv_data to return our sample data
    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        display_filtered_table(csv_file_name="products.csv", search_target="Banana")
        captured = capsys.readouterr()

    expected_output = "['Product', 'Price', 'Quantity']\n" \
                      "['Banana', '0.5', '20']"

    assert captured.out.strip() == expected_output

def test_display_filtered_table_with_empty_search(capsys):
    # Sample CSV data with headers and some products
    header = ["Product", "Price", "Quantity"]
    csv_reader = [
        ["Apple", "1.2", "10"],
        ["Banana", "0.5", "20"],
        ["Orange", "0.8", "15"]
    ]
    # Mocking get_csv_data to return our sample data
    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        display_filtered_table(csv_file_name="products.csv", search_target="")
        captured = capsys.readouterr()

    expected_output = "['Product', 'Price', 'Quantity']"

    assert captured.out.strip() == expected_output

def test_display_filtered_table_single_product(capsys):
    # Sample CSV data with a single product
    header = ["Product", "Price", "Quantity"]
    csv_reader = [
        ["Apple", "1.2", "10"]
    ]
    # Mocking get_csv_data to return our sample data
    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        display_filtered_table(csv_file_name="products.csv", search_target=None)
        captured = capsys.readouterr()

    expected_output = "['Product', 'Price', 'Quantity']\n" \
                      "['Apple', '1.2', '10']"

    assert captured.out.strip() == expected_output

def test_display_filtered_table_same_product_name(capsys):
    # Sample CSV data with the same product name but different prices/quantities
    header = ["Product", "Price", "Quantity"]
    csv_reader = [
        ["Apple", "1.2", "10"],
        ["Apple", "0.5", "20"],
        ["Apple", "0.8", "15"]
    ]
    # Mocking get_csv_data to return our sample data
    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        display_filtered_table(csv_file_name="products.csv", search_target="Apple")
        captured = capsys.readouterr()

    expected_output = "['Product', 'Price', 'Quantity']\n" \
                      "['Apple', '1.2', '10']\n" \
                      "['Apple', '0.5', '20']\n" \
                      "['Apple', '0.8', '15']"

    assert captured.out.strip() == expected_output

def test_display_filtered_table_special_characters(capsys):
    # Sample CSV data with special characters in the product names
    header = ["Product", "Price", "Quantity"]
    csv_reader = [
        ["Apple@2021", "1.2", "10"],
        ["Banana$special", "0.5", "20"],
        ["Orange&fresh", "0.8", "15"]
    ]
    # Mocking get_csv_data to return our sample data
    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        display_filtered_table(csv_file_name="products.csv", search_target=None)
        captured = capsys.readouterr()

    expected_output = "['Product', 'Price', 'Quantity']\n" \
                      "['Apple@2021', '1.2', '10']\n" \
                      "['Banana$special', '0.5', '20']\n" \
                      "['Orange&fresh', '0.8', '15']"

    assert captured.out.strip() == expected_output


# Test when no search target is provided, all product data should be shown
def test_display_filtered_table_no_search_target(capsys):
    # Sample CSV data with headers and some products
    header = ["Product", "Price", "Quantity"]
    csv_reader = [
        ["Apple", "1.2", "10"],
        ["Banana", "0.5", "20"],
        ["Orange", "0.8", "15"]
    ]

    # Mocking get_csv_data to return our sample data
    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        # Calling display_filtered_table without providing a search target
        display_filtered_table(csv_file_name="products.csv", search_target=None)

        # Capturing the output
        captured = capsys.readouterr()

    # Expected output should include all products
    expected_output = "['Product', 'Price', 'Quantity']\n" \
                      "['Apple', '1.2', '10']\n" \
                      "['Banana', '0.5', '20']\n" \
                      "['Orange', '0.8', '15']"

    assert captured.out.strip() == expected_output


# Test when a search target is provided, only matching products should be displayed
def test_display_filtered_table_with_search_target(capsys):
    # Sample CSV data with headers and some products
    header = ["Product", "Price", "Quantity"]
    csv_reader = [
        ["Apple", "1.2", "10"],
        ["Banana", "0.5", "20"],
        ["Orange", "0.8", "15"]
    ]

    # Mocking get_csv_data to return our sample data
    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        # Calling display_filtered_table, searching for "Apple"
        display_filtered_table(csv_file_name="products.csv", search_target="Apple")

        # Capturing the output
        captured = capsys.readouterr()

    # Expected output should only include the "Apple" product
    expected_output = "['Product', 'Price', 'Quantity']\n" \
                      "['Apple', '1.2', '10']"

    assert captured.out.strip() == expected_output


# Test when no product matches the search target, nothing should be displayed
def test_display_filtered_table_no_match(capsys):
    # Sample CSV data with headers and some products
    header = ["Product", "Price", "Quantity"]
    csv_reader = [
        ["Apple", "1.2", "10"],
        ["Banana", "0.5", "20"],
        ["Orange", "0.8", "15"]
    ]

    # Mocking get_csv_data to return our sample data
    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        # Calling display_filtered_table, searching for "Pineapple" (no matching product)
        display_filtered_table(csv_file_name="products.csv", search_target="Pineapple")

        # Capturing the output
        captured = capsys.readouterr()

    # Expected output should only include the header, no product data
    expected_output = "['Product', 'Price', 'Quantity']"

    # Stripping to remove trailing newlines and comparing
    assert captured.out.strip().splitlines()[0] == expected_output


# Test case-insensitive matching, it should return the matching products
def test_display_filtered_table_case_insensitive(capsys):
    # Sample CSV data with headers and some products
    header = ["Product", "Price", "Quantity"]
    csv_reader = [
        ["Apple", "1.2", "10"],
        ["Banana", "0.5", "20"],
        ["Orange", "0.8", "15"]
    ]

    # Mocking get_csv_data to return our sample data
    with patch("online_shopping_cart.product.product_search.get_csv_data", return_value=(header, csv_reader)):
        # Calling display_filtered_table, searching for "apple" (case-insensitive)
        display_filtered_table(csv_file_name="products.csv", search_target="apple")

        # Capturing the output
        captured = capsys.readouterr()

    # Expected output should include the "Apple" product (case-insensitive)
    expected_output = "['Product', 'Price', 'Quantity']\n" \
                      "['Apple', '1.2', '10']"

    assert captured.out.strip() == expected_output


# Test invalid input


# Test invalid input: Invalid csv_file_name (float type)
def test_invalid_csv_file_name_float(capsys):
    # Add print statement to confirm the input type
    print(f"Testing with csv_file_name = 12.34 (type: {type(12.34)})")  # Debug line

    # Ensure we are capturing the correct TypeError with the expected message
    with pytest.raises(TypeError, match="File name must be a string"):
        display_filtered_table(csv_file_name=12.34, search_target=None)


# Test invalid input: Invalid csv_file_name (list type)
def test_invalid_csv_file_name_list(capsys):
    with pytest.raises(TypeError, match=r"File name must be a string"):
        display_filtered_table(csv_file_name=['invalid', 'list'], search_target=None)




def test_invalid_csv_file_name_int(capsys):
    """Test invalid input: Integer as file name"""
    with pytest.raises(TypeError, match="File name must be a string"):
        display_filtered_table(csv_file_name=123, search_target=None)

# Test invalid input: Invalid csv_file_name (None type)
def test_invalid_csv_file_name_none(capsys):
    with pytest.raises(TypeError, match="File name must be a string"):
        display_filtered_table(csv_file_name=None, search_target=None)
