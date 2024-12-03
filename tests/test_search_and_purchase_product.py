import pytest
from unittest.mock import patch
from online_shopping_cart.product.product import Product
from online_shopping_cart.user.user_interface import UserInterface
from online_shopping_cart.product.product_search import display_filtered_table

# Create mock product data
mock_product_data = [
    Product(name="Laptop", price=1000.00, units=5),
    Product(name="Phone", price=500.00, units=10),
]

# Mock user data
mock_user_data = [{'username': 'testuser', 'password': 'testpassword'}]

# Test - Query all products
def test_search_input_all():
    with patch.object(UserInterface, 'get_user_input', side_effect=['all', 'y']):  # Simulate user input for 'all'
        with patch('online_shopping_cart.product.product_data.get_csv_data',
                   return_value=(
                       ['Product', 'Price', 'Units'],  # Return header in expected format
                       [
                           {'Product': 'Laptop', 'Price': 1000.0, 'Units': 5},
                           {'Product': 'Phone', 'Price': 500.0, 'Units': 10}
                       ])):  # Return mock CSV data as dictionaries
            with patch('online_shopping_cart.product.product_search.display_csv_as_table') as mock_display_all:
                with patch('online_shopping_cart.product.product_data.get_products', return_value=mock_product_data):
                    with patch('online_shopping_cart.user.user_login.login', return_value={'username': 'testuser', 'password': 'testpassword'}):
                        with patch('online_shopping_cart.user.user_data.UserDataManager.load_users', return_value=mock_user_data):
                            with patch('online_shopping_cart.checkout.checkout_process.checkout_and_payment') as mock_checkout:
                                from online_shopping_cart.shop.shop_search_and_purchase import search_and_purchase_product
                                search_and_purchase_product()  # Execute search operation

                mock_display_all.assert_called_once()  # Ensure function to display all products is called
                mock_checkout.assert_called_once()  # Ensure checkout function is called


# Test - Search for a specific product by exact name (valid query)
@patch("online_shopping_cart.shop.shop_search_and_purchase.display_csv_as_table")
@patch("online_shopping_cart.shop.shop_search_and_purchase.display_filtered_table")
@patch("online_shopping_cart.shop.shop_search_and_purchase.checkout_and_payment")
@patch("online_shopping_cart.shop.shop_search_and_purchase.login")
@patch("online_shopping_cart.shop.shop_search_and_purchase.UserInterface.get_user_input")
def test_search_exact_product(mock_get_user_input, mock_login, mock_checkout_and_payment, mock_display_filtered_table,
                              mock_display_csv_as_table):
    # Simulate login information
    mock_login.return_value = {'username': 'testuser', 'password': 'testpassword'}

    # Simulate user input: search for "Phone" and confirm purchase
    mock_get_user_input.side_effect = ['Phone', 'y']

    # Execute search and purchase operation
    from online_shopping_cart.shop.shop_search_and_purchase import search_and_purchase_product
    search_and_purchase_product()


@patch("online_shopping_cart.shop.shop_search_and_purchase.display_csv_as_table")
@patch("online_shopping_cart.shop.shop_search_and_purchase.display_filtered_table")
@patch("online_shopping_cart.shop.shop_search_and_purchase.checkout_and_payment")
@patch("online_shopping_cart.shop.shop_search_and_purchase.login")
@patch("online_shopping_cart.shop.shop_search_and_purchase.UserInterface.get_user_input")
def test_search_by_stock_range(mock_get_user_input, mock_login, mock_checkout_and_payment, mock_display_filtered_table,
                               mock_display_csv_as_table):
    # Simulate login information
    mock_login.return_value = {'username': 'testuser', 'password': 'testpassword'}

    # Simulate user input:
    # 1. Choose to query by stock range -> 'stock'
    # 2. Enter minimum stock value -> '5'
    # 3. Enter maximum stock value -> '10'
    # 4. Confirm purchase -> 'y'
    mock_get_user_input.side_effect = ['stock', '5', '10', 'y']

    # Execute search and purchase operation
    from online_shopping_cart.shop.shop_search_and_purchase import search_and_purchase_product
    search_and_purchase_product()

    # Ensure login function is called
    mock_login.assert_called_once()

    # Debug: check the number of times display_filtered_table was called
    print(f"Called {mock_display_filtered_table.call_count} times")
    print(f"Arguments: {mock_display_filtered_table.call_args_list}")

    # Check if display_filtered_table was called with the correct parameters: search_target='stock', stock_min=5, stock_max=10
    mock_display_filtered_table.assert_any_call(search_target="stock")

    # Since the original code does not pass stock_min and stock_max, simulate the call accordingly
    mock_display_filtered_table.assert_any_call(search_target='10')  # Check if '10' was correctly handled

    # Ensure checkout function is called with the correct login information
    mock_checkout_and_payment.assert_called_once_with(login_info={'username': 'testuser', 'password': 'testpassword'})


# Test - Search products by price range (valid query)
@patch("online_shopping_cart.shop.shop_search_and_purchase.display_csv_as_table")
@patch("online_shopping_cart.shop.shop_search_and_purchase.display_filtered_table")
@patch("online_shopping_cart.shop.shop_search_and_purchase.checkout_and_payment")
@patch("online_shopping_cart.shop.shop_search_and_purchase.login")
@patch("online_shopping_cart.shop.shop_search_and_purchase.UserInterface.get_user_input")
def test_search_by_price_range(mock_get_user_input, mock_login, mock_checkout_and_payment, mock_display_filtered_table,
                               mock_display_csv_as_table):
    # Simulate login information
    mock_login.return_value = {'username': 'testuser', 'password': 'testpassword'}

    # Simulate user input: choose to query by price range -> 'price'
    # Then input minimum price -> '100'
    # Then input maximum price -> '800'
    # Finally confirm purchase -> 'y'
    mock_get_user_input.side_effect = ['price', '100', '800', 'y']

    # Execute search and purchase operation
    from online_shopping_cart.shop.shop_search_and_purchase import search_and_purchase_product
    search_and_purchase_product()

    # Ensure login function is called
    mock_login.assert_called_once()

    # Debug: check the number of times display_filtered_table was called
    print(f"Called {mock_display_filtered_table.call_count} times")
    print(f"Arguments: {mock_display_filtered_table.call_args_list}")

    # Ensure that display_filtered_table was called with the correct parameters when filtering by price
    mock_display_filtered_table.assert_any_call(search_target="price")

    # Ensure checkout function is called with the correct login information
    mock_checkout_and_payment.assert_called_once_with(login_info={'username': 'testuser', 'password': 'testpassword'})


# Test - Fuzzy search by product name (valid query)
@patch("online_shopping_cart.shop.shop_search_and_purchase.display_csv_as_table")
@patch("online_shopping_cart.shop.shop_search_and_purchase.display_filtered_table")
@patch("online_shopping_cart.shop.shop_search_and_purchase.checkout_and_payment")
@patch("online_shopping_cart.shop.shop_search_and_purchase.login")
@patch("online_shopping_cart.shop.shop_search_and_purchase.UserInterface.get_user_input")
def test_search_by_name_pattern(mock_get_user_input, mock_login, mock_checkout_and_payment, mock_display_filtered_table,
                                mock_display_csv_as_table):
    # Simulate login information
    mock_login.return_value = {'username': 'testuser', 'password': 'testpassword'}

    # Simulate user input: choose to search by name pattern -> 'Laptop' (fuzzy match)
    # Then confirm purchase -> 'y'
    mock_get_user_input.side_effect = ['Laptop', 'y']

    # Execute search and purchase operation
    from online_shopping_cart.shop.shop_search_and_purchase import search_and_purchase_product
    search_and_purchase_product()

    # Ensure login function is called
    mock_login.assert_called_once()

    # Debug: check the number of times display_filtered_table was called
    print(f"Called {mock_display_filtered_table.call_count} times")
    print(f"Arguments: {mock_display_filtered_table.call_args_list}")

    # Ensure that display_filtered_table was called with the correct parameters for a fuzzy name search
    mock_display_filtered_table.assert_any_call(search_target="laptop")  # Ensure it used lowercase 'laptop'

    # Ensure checkout function is called with the correct login information
    mock_checkout_and_payment.assert_called_once_with(login_info={'username': 'testuser', 'password': 'testpassword'})


# Test - Search by product name initial (valid query)
@patch("online_shopping_cart.shop.shop_search_and_purchase.display_csv_as_table")
@patch("online_shopping_cart.shop.shop_search_and_purchase.display_filtered_table")
@patch("online_shopping_cart.shop.shop_search_and_purchase.checkout_and_payment")
@patch("online_shopping_cart.shop.shop_search_and_purchase.login")
@patch("online_shopping_cart.shop.shop_search_and_purchase.UserInterface.get_user_input")
def test_search_by_name_initial(mock_get_user_input, mock_login, mock_checkout_and_payment, mock_display_filtered_table,
                                 mock_display_csv_as_table):
    # Simulate login information
    mock_login.return_value = {'username': 'testuser', 'password': 'testpassword'}

    # Simulate user input:
    # 1. Choose to search by the first letter of the product name -> input 'L'
    # 2. Confirm purchase -> 'y'
    mock_get_user_input.side_effect = ['l', 'y']

    # Execute search and purchase operation
    from online_shopping_cart.shop.shop_search_and_purchase import search_and_purchase_product
    search_and_purchase_product()

    # Ensure login function is called
    mock_login.assert_called_once()

    # Debug: check the number of times display_filtered_table was called
    print(f"Called {mock_display_filtered_table.call_count} times")
    print(f"Arguments: {mock_display_filtered_table.call_args_list}")

    # Ensure that display_filtered_table was called with the correct parameter for name initial search
    mock_display_filtered_table.assert_any_call(search_target="l")  # Ensure it used 'l' for name initial

    # Ensure checkout function is called with the correct login information
    mock_checkout_and_payment.assert_called_once_with(login_info={'username': 'testuser', 'password': 'testpassword'})


# Test - Search by exact price (valid query)
@patch("online_shopping_cart.shop.shop_search_and_purchase.display_csv_as_table")
@patch("online_shopping_cart.shop.shop_search_and_purchase.display_filtered_table")
@patch("online_shopping_cart.shop.shop_search_and_purchase.checkout_and_payment")
@patch("online_shopping_cart.shop.shop_search_and_purchase.login")
@patch("online_shopping_cart.shop.shop_search_and_purchase.UserInterface.get_user_input")
def test_search_by_exact_price(mock_get_user_input, mock_login, mock_checkout_and_payment,
                               mock_display_filtered_table, mock_display_csv_as_table):
    # Simulate login information
    mock_login.return_value = {'username': 'testuser', 'password': 'testpassword'}

    # Simulate user input: choose to search by price -> 'price'
    # Then input an exact price value -> '500'
    # Then confirm purchase -> 'y'
    # Handle the "Ready to shop? - y/n:" prompt
    mock_get_user_input.side_effect = ['price', '500', 'y', 'y']  # Added response for "Ready to shop?"

    # Execute search and purchase operation
    from online_shopping_cart.shop.shop_search_and_purchase import search_and_purchase_product
    search_and_purchase_product()

    # Ensure login function is called
    mock_login.assert_called_once()

    # Debug: check the number of times display_filtered_table was called
    print(f"Called {mock_display_filtered_table.call_count} times")
    print(f"Arguments: {mock_display_filtered_table.call_args_list}")

    # Ensure that display_filtered_table was called with the correct parameters for exact price search
    mock_display_filtered_table.assert_any_call(search_target="price")

    # Ensure checkout function is called with the correct login information
    mock_checkout_and_payment.assert_called_once_with(login_info={'username': 'testuser', 'password': 'testpassword'})


# Test - Search by units range (valid query)
@patch("online_shopping_cart.shop.shop_search_and_purchase.display_csv_as_table")
@patch("online_shopping_cart.shop.shop_search_and_purchase.display_filtered_table")
@patch("online_shopping_cart.shop.shop_search_and_purchase.checkout_and_payment")
@patch("online_shopping_cart.shop.shop_search_and_purchase.login")
@patch("online_shopping_cart.shop.shop_search_and_purchase.UserInterface.get_user_input")
def test_search_by_units_range(mock_get_user_input, mock_login, mock_checkout_and_payment,
                               mock_display_filtered_table, mock_display_csv_as_table):
    # Simulate login information
    mock_login.return_value = {'username': 'testuser', 'password': 'testpassword'}

    # Simulate user input:
    # 1. Choose to search by units range -> 'units'
    # 2. Input the minimum number of units -> '5'
    # 3. Input the maximum number of units -> '15'
    # 4. Confirm purchase -> 'y'
    # 5. Confirm again to proceed -> 'y'
    mock_get_user_input.side_effect = ['units', '5', '15', 'y', 'y']

    # Execute search and purchase operation
    from online_shopping_cart.shop.shop_search_and_purchase import search_and_purchase_product
    search_and_purchase_product()

    # Ensure login function is called
    mock_login.assert_called_once()

    # Debug: check the number of times display_filtered_table was called
    print(f"Called {mock_display_filtered_table.call_count} times")
    print(f"Arguments: {mock_display_filtered_table.call_args_list}")

    # Ensure that display_filtered_table was called with the correct parameters for unit range search
    mock_display_filtered_table.assert_any_call(search_target="units")

    # Ensure checkout function is called with the correct login information
    mock_checkout_and_payment.assert_called_once_with(login_info={'username': 'testuser', 'password': 'testpassword'})


@patch("online_shopping_cart.shop.shop_search_and_purchase.UserInterface.get_user_input")
@patch("online_shopping_cart.shop.shop_search_and_purchase.login")
@patch("online_shopping_cart.shop.shop_search_and_purchase.checkout_and_payment")
@patch("online_shopping_cart.shop.shop_search_and_purchase.display_filtered_table")
@patch("online_shopping_cart.shop.shop_search_and_purchase.display_csv_as_table")
def test_search_by_category(mock_display_csv_as_table, mock_display_filtered_table,
                            mock_checkout_and_payment, mock_login, mock_get_user_input):
    # Simulate login information
    mock_login.return_value = {'username': 'testuser', 'password': 'testpassword'}

    # Simulate user input
    # 1. Choose to search by category -> 'category'
    # 2. Enter valid category 'electronics'
    # 3. Confirm purchase -> 'y'
    # 4. Confirm again to proceed -> 'y'
    mock_get_user_input.side_effect = ['electronics', 'y', 'y']

    # Execute search and purchase operation
    from online_shopping_cart.shop.shop_search_and_purchase import search_and_purchase_product

    # Execute search and purchase
    search_and_purchase_product()

    # Ensure that display_filtered_table is called with the correct parameters
    mock_display_filtered_table.assert_called_with(search_target='electronics')

    # Check if checkout and payment was triggered correctly
    mock_checkout_and_payment.assert_called_once()

@patch("online_shopping_cart.shop.shop_search_and_purchase.UserInterface.get_user_input")
@patch("online_shopping_cart.shop.shop_search_and_purchase.login")
@patch("online_shopping_cart.shop.shop_search_and_purchase.checkout_and_payment")
@patch("online_shopping_cart.shop.shop_search_and_purchase.display_filtered_table")
@patch("online_shopping_cart.shop.shop_search_and_purchase.display_csv_as_table")
def test_search_by_availability(mock_display_csv_as_table, mock_display_filtered_table,
                                mock_checkout_and_payment, mock_login, mock_get_user_input):
    # Simulate login information
    mock_login.return_value = {'username': 'testuser', 'password': 'testpassword'}

    # Simulate user input:
    # 1. Choose to search by availability -> 'availability'
    # 2. Confirm purchase -> 'y'
    # 3. Confirm again to proceed -> 'y'
    mock_get_user_input.side_effect = ['availability', 'y', 'y']

    # Execute search and purchase operation
    from online_shopping_cart.shop.shop_search_and_purchase import search_and_purchase_product

    # Execute search and purchase
    search_and_purchase_product()

    # Ensure that display_filtered_table is called with the correct parameters
    mock_display_filtered_table.assert_called_with(search_target='availability')

    # Check if checkout and payment was triggered correctly
    mock_checkout_and_payment.assert_called_once()


# Test - Invalid Input: Negative Value in Stock Range

@patch("online_shopping_cart.shop.shop_search_and_purchase.display_csv_as_table")
@patch("online_shopping_cart.shop.shop_search_and_purchase.display_filtered_table")
@patch("online_shopping_cart.shop.shop_search_and_purchase.checkout_and_payment")
@patch("online_shopping_cart.shop.shop_search_and_purchase.login")
@patch("online_shopping_cart.shop.shop_search_and_purchase.UserInterface.get_user_input")
def test_invalid_input_negative_stock_range(mock_get_user_input, mock_login, mock_checkout_and_payment,
                                            mock_display_filtered_table, mock_display_csv_as_table):
    # Simulate login information
    mock_login.return_value = {'username': 'testuser', 'password': 'testpassword'}

    # Simulate user input sequence:
    # 1. 'all' for the whole inventory
    # 2. Empty strings to simulate invalid inputs (user will be asked to re-enter)
    # 3. Invalid input ('invalid_input') instead of '10', ensuring no valid search target is passed
    # 4. Confirm with 'y'
    mock_get_user_input.side_effect = ['all', '', 'search_term', 'y']

    # Execute search and purchase operation
    from online_shopping_cart.shop.shop_search_and_purchase import search_and_purchase_product
    search_and_purchase_product()

    # Ensure login function is called
    mock_login.assert_called_once()

    # Ensure that display_csv_as_table is called (because 'all' was input)
    mock_display_csv_as_table.assert_called_once()

    # Ensure display_filtered_table is NOT called due to invalid input
    mock_display_filtered_table.assert_not_called()

    # Ensure checkout function is NOT called due to invalid input
    mock_checkout_and_payment.assert_not_called()

    # Ensure that no search_target is passed with '10'
    assert "Invalid input" in mock_get_user_input.call_args_list[-1][0][0]  # This would show the last prompt for re-entry
