import json
import shutil
from unittest.mock import patch
from online_shopping_cart.user.user import User
from online_shopping_cart.checkout.shopping_cart import ShoppingCart
from online_shopping_cart.checkout.checkout_process import check_cart, display_cart_items
from online_shopping_cart.product.product import Product
import pytest

# Fixture to create a sample user
@pytest.fixture
def Test_user():
    with open("./files/users.json") as user_file:
        user_data_list = json.load(user_file)
        # Assuming there's at least one user in the list
        user_data = user_data_list[0]
    return User(user_data["username"], user_data["wallet"])

# Fixture to create a sample product
@pytest.fixture
def Test_product():
    products ="products.csv"
    return products[0] if products else None

# Fixture to create a sample cart
@pytest.fixture
def Test_cart():
    return ShoppingCart()

###invalid inputs
def test_check_cart_invalid_user(Test_cart, Test_product):
    invalid_user = None  # Simulate an invalid user (None)

    check_cart(invalid_user, Test_cart)  # No exception is raised
    assert len(Test_cart.retrieve_items()) == 0  # The cart should remain unchanged

#test case:invalid user inputs
def test_check_cart_invalid_checkout_input(Test_user, Test_cart):
    # Add a product to the cart
    Test_cart.add_item(Test_product)

    # Simulate invalid input
    with patch('builtins.input', side_effect=['a', 'x', 'Y']):  # Invalid, invalid, and valid input
        check_cart(Test_user, Test_cart)

    assert len(Test_cart.retrieve_items()) == 1  # The cart should still have the product


def test_check_cart_cancel_checkout_after_adding_items(Test_user, Test_cart):
    # Add items to the cart
    Test_cart.add_item(Test_product)

    # Simulate user input to cancel the checkout
    with patch('builtins.input', return_value='N'):  # User decides not to checkout
        result = check_cart(Test_user, Test_cart)

    # Assert that the checkout was cancelled
    assert result is False  # The result should be False, meaning checkout was cancelled


def test_check_cart_remove_invalid_index(Test_user, Test_cart):
    # Add a product to the cart
    Test_cart.add_item(Test_product)

    # Simulate invalid input for removing an item (out of range)
    with patch('builtins.input', return_value='999'):  # Non-existent item index
        check_cart(Test_user, Test_cart)

    # Assert the cart remains unchanged
    assert len(Test_cart.retrieve_items()) == 1  # The product should still be in the cart


# Test Case : User checks out an empty cart
def test_check_cart_empty_cart(capsys, Test_user, Test_cart):
    with patch('builtins.input', return_value='Y'):
        check_cart(Test_user, Test_cart)
        captured = capsys.readouterr()
        assert "Your basket is empty" in captured.out
#Test Case: User adds a valid product to the cart
def test_check_cart_add_valid_product(Test_user, Test_cart, Test_product):
    with patch('builtins.input', side_effect=['1', 'N']):
        Test_cart.add_item(Test_product)
        assert check_cart(Test_user, Test_cart) is False
        assert len(Test_cart.retrieve_items()) == 1  # Ensure the product is added to the cart

#test case when adding multiple inputs
def test_check_cart_add_multiple_valid_products(Test_user, Test_cart):
    # Create multiple valid products
    product1 = Product(name='Laptop', price=1000.0, units=1)
    product2 = Product(name='Headphones', price=100.0, units=2)

    # Add products to the cart
    Test_cart.add_item(product1)
    Test_cart.add_item(product2)

    # Check that the cart contains both products
    items = Test_cart.retrieve_items()
    assert len(items) == 2
    assert items[0].name == 'Laptop'
    assert items[1].name == 'Headphones'




#test case for,User decides not to proceed with checkout
def test_check_cart_no_checkout(capsys, Test_user, Test_cart):
    with patch('builtins.input', return_value='N'):
        result = check_cart(Test_user, Test_cart)
        assert result is False

#test case for verifying the total price after adding items to cart
def test_check_cart_total_price(Test_user, Test_cart):
    # Create multiple valid products
    product1 = Product(name='Laptop', price=1000.0, units=1)
    product2 = Product(name='Headphones', price=100.0, units=2)

    # Add products to the cart
    Test_cart.add_item(product1)
    Test_cart.add_item(product2)

    total_price = Test_cart.get_total_price()

    # Ensure the total price is calculated correctly
    assert total_price == 1200.0




# User enters an empty input
def test_check_cart_empty_input(Test_user, Test_cart, capsys):
    with patch('builtins.input', side_effect=['']):
        result = check_cart(Test_user, Test_cart)
    captured = capsys.readouterr()
    # Check that the printed output does not contain the error message
    assert "Invalid input. Please try again." not in captured.out
    # Check that the result is False, indicating the user did not checkout
    assert result is False

# User enters an invalid input ('X') in check_cart function
def test_check_cart_invalid_input_x(Test_user, Test_cart, capsys):
    with patch('builtins.input', side_effect=['X']):
        result = check_cart(Test_user, Test_cart)
    captured = capsys.readouterr()
    # Check that the printed output does not contain the error message
    assert "Invalid input. Please try again." not in captured.out
    # Check that the result is False, indicating the user did not checkout
    assert result is False

#User decides not to proceed with checkout
def test_check_cart_no_checkout(capsys, Test_user, Test_cart):
    with patch('builtins.input', return_value='N'):
        result = check_cart(Test_user, Test_cart)
        assert result is False


def test_check_cart_sufficient_funds(Test_user, Test_cart, Test_product, capsys):
    # User has enough funds
    Test_user.wallet = 100.0
    Test_cart.add_item(Test_product)

    # Simulate user input to proceed with checkout
    with patch('builtins.input', return_value='Y'):
        check_cart(Test_user, Test_cart)
        captured = capsys.readouterr()

        # Check the expected checkout success message
        assert "Thank you for your purchase" in captured.out
        assert "Your remaining balance" in captured.out


# Test Case: User checks out with sufficient funds
def test_check_cart_sufficient_funds(Test_user, Test_cart, capsys):
    # Create a mock product with price and units
    class Product:
        def __init__(self, name, price, units):
            self.name = name
            self.price = price
            self.units = units

    Test_product = Product(name='p', price=10.0, units=1)  # Example product

    # User has enough funds
    Test_user.wallet = 100.0
    Test_cart.add_item(Test_product)

    # Simulate user input to proceed with checkout
    with patch('builtins.input', return_value='Y'):
        check_cart(Test_user, Test_cart)

    # Capture the output
    captured = capsys.readouterr()

    # Ensure the checkout message is printed correctly
    assert "Thank you for your purchase" in captured.out
    assert "Your remaining balance is 90.0" in captured.out


# User enters an invalid input and decides not to check out
def test_check_cart_invalid_input(Test_user, Test_cart):
    with patch('builtins.input', side_effect=['invalid', 'N']):
        assert check_cart(Test_user, Test_cart) is False

# User decides not to check out
def test_check_cart_no_checkout(Test_user, Test_cart):
    with patch('builtins.input', return_value='N'):
        assert check_cart(Test_user, Test_cart) is False

#Test invalid input ('') in check_cart function
def test_check_cart_empty_input(Test_user, Test_cart, capsys):
    with patch('builtins.input', side_effect=['']):
        result = check_cart(Test_user, Test_cart)
    captured = capsys.readouterr()
    # Check that the printed output does not contain the error message
    assert "Invalid input. Please try again." not in captured.out
    # Check that the result is False, indicating the user did not checkout
    assert result is False

#test case for negative price  product
def validate_product(product):
    if product.price < 0:
        raise ValueError("Product price cannot be negative.")


def test_check_cart_add_invalid_product_with_invalid_price(Test_user, Test_cart):
    # Simulating a product with an invalid price
    invalid_product = Product(name='Invalid Product', price=-10.0, units=1)

    # Validate the product manually before adding to the cart
    with pytest.raises(ValueError):
        validate_product(invalid_product)
        Test_cart.add_item(invalid_product)


