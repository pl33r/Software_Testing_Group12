import pytest
import json
from unittest.mock import patch, mock_open
from online_shopping_cart.checkout.checkout_process import checkout
from online_shopping_cart.product.product import Product
from online_shopping_cart.checkout.shopping_cart import ShoppingCart
from online_shopping_cart.user.user import User


# Mock data for products.csv
mock_products_csv_data = """Product,Price,Units
Apple,2,10
Banana,1,15
"""

# Mock data for users.json
mock_users_json_data = """
[
  {
    "username": "Ramanathan",
    "password": "Notaproblem23*",
    "wallet": 100.0
  },
  {
    "username": "Samantha",
    "password": "SecurePass123/^",
    "wallet": 150.0
  }
]
"""

@pytest.fixture
def mock_products_csv():
    with patch('builtins.open', mock_open(read_data=mock_products_csv_data)):
        yield


@pytest.fixture
def mock_users_json():
    with patch('builtins.open', mock_open(read_data=mock_users_json_data)):
        yield


@pytest.fixture
def mock_user(mock_users_json):
    # Load user data from the mocked users.json file
    users = json.loads(mock_users_json_data)  #loading the mock data
    user_data = users[0]  # Use the first user for an eg
    return User(name=user_data['username'], wallet=user_data['wallet'])

###invalid inputs
#test for negative wallet balance
def test_negative_wallet_balance():
    user = User(name="Zara", wallet=-10.0)  # Invalid balance(-ve)
    cart = ShoppingCart()
    cart.add_item(Product(name="Apple", price=2, units=5))  # Total =10(2*5)
    checkout(user, cart)
    assert user.wallet == -10.0  # The wallet balance is negative
    assert not cart.is_empty()  # Cart is not cleared as the user can't afford the product
#test for zero price and quantity
def test_zero_price_and_quantity():
    user = User(name="Rover", wallet=100.0)
    cart = ShoppingCart()
    # Adding a product to cart with both zero price and zero quantity
    cart.add_item(Product(name="FreeProduct", price=0, units=0))
    checkout(user, cart)
    assert user.wallet == 100.0  # No change in wallet as the product is invalid
    assert cart.is_empty()  # Cart should be cleared after checkout
#test for empty cart
def test_checkout_with_empty_cart():
    user = User(name="Phoenix", wallet=100.0)
    cart = ShoppingCart()
    checkout(user, cart)
    assert user.wallet == 100.0  # Wallet balance should remain unchanged as no products were bought
    assert cart.is_empty()  # Cart is already empty


#test case for checking the correctness the checkout function
def test_checkout_function(mock_products_csv, mock_user):
    # Setup the cart and products
    cart = ShoppingCart()
    selected_product = Product(name="Apple", price=2, units=10)
    cart.add_item(selected_product)  # Adding 1 Apple to the cart

    print(f"Initial wallet balance: {mock_user.wallet}")  # Debugging line before checkout

    # Test the checkout
    checkout(mock_user, cart)

    print(f"Total cost of products: {selected_product.price * selected_product.units}")  # Debugging line
    print(f"Final wallet balance: {mock_user.wallet}")  # Debugging line

    # After checkout, the user's wallet should decrease by the total price
    assert mock_user.wallet == 80.0
    assert cart.is_empty()  # Cart should be cleared after checkout

#Test Case for valid checkout
def test_valid_checkout():
    # Create a user using the correct attributes 'name' and 'wallet'
    user = User(name="Ramanathan", wallet=100.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Apple", price=2, units=10))  # Adding 10 Apples at $2 as unit price

    checkout(user, cart)

    # The wallet should decrease by the total cost of the items
    assert user.wallet == 80.0 #(100-20)
    assert cart.is_empty()
#Test Case for Single Product, Sufficient Wallet Balance
def test_single_product_checkout():
    user = User(name="Ramanathan", wallet=100.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Banana", price=3, units=5))
    checkout(user, cart)
    assert user.wallet == 85.0
    assert cart.is_empty()  # Cart should be cleared after checkout

# multiple Product, Sufficient Wallet Balance
def test_multiple_products_checkout():
    user = User(name="Samantha", wallet=150.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Apple", price=2, units=10))  # 10 Apples at $2 per unit
    cart.add_item(Product(name="Orange", price=1.5, units=10))  # 10 Oranges at $1.5 per unit
    checkout(user, cart)
    assert user.wallet == 115.0
    assert cart.is_empty()


#Test Case for wallet Balance Exactly Matching Total Cost
def test_exact_wallet_balance():
    # Create a user whose wallet exactly matches the total cost
    user = User(name="Maximus", wallet=10.0)
    cart = ShoppingCart()

    # Add items to the cart with a total price equal to the wallet balance
    cart.add_item(Product(name="Apple", price=2, units=5))
    checkout(user, cart)

    assert user.wallet == 0.0  # Wallet should be exactly 0 after checkout
    assert cart.is_empty()

#Test Case for Large Quantity of Single Product
def test_large_quantity_checkout():
    user = User(name="Aria", wallet=500.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Banana", price=1, units=100))
    checkout(user, cart)
    assert user.wallet == 400.0
    assert cart.is_empty()
#Test Case for Empty Cart Checkout
def test_empty_cart_checkout():
    user = User(name="Luna", wallet=100.0)
    cart = ShoppingCart()
    checkout(user, cart)  # Checkout with an empty cart
    assert user.wallet == 100.0  # No change in wallet balance

 #Test Case for insufficient Balance with Expensive Product
def test_small_wallet_balance_expensive_product():
    user = User(name="Rover", wallet=50.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Laptop", price=300, units=1))  # 1 Laptop at $300
    checkout(user, cart)
    assert user.wallet == 50.0  # no change in user wallet, as user cant afford the product
    assert not cart.is_empty()  # Cart shouldn't be cleared as checkout was unsuccessful
#Test Case for Exact Product Price with Exact Wallet Balance
def test_exact_product_price_wallet_balance():
    user = User(name="Felix", wallet=80.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Smartphone", price=80.0, units=1))
    checkout(user, cart)
    assert user.wallet == 0.0  # Wallet balance should be reduced to 0 after checkout
    assert cart.is_empty()

#Test Case for product with zero price
def test_zero_price_product():
    user = User(name="Zara", wallet=100.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="FreeProduct", price=0, units=5))  # 5 Free Products
    checkout(user, cart)
    assert user.wallet == 100.0
    assert cart.is_empty()

#Test Case for Multiple Products, Exact Total Match with Wallet
def test_multiple_products_exact_total():
    user = User(name="Tiger", wallet=200.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Apple", price=5, units=10))
    cart.add_item(Product(name="Banana", price=5, units=10))
    checkout(user, cart)
    assert user.wallet == 100.0
    assert cart.is_empty()

# Test Case for Zero Wallet Balance
def test_zero_wallet_balance():
    user = User(name="Oliver", wallet=0.0)  # User has no money in wallet
    cart = ShoppingCart()
    cart.add_item(Product(name="Apple", price=5, units=5))
    checkout(user, cart)
    assert user.wallet == 0.0
    assert not cart.is_empty() #cart shouldnt be cleared as checkout was unsuccessful



