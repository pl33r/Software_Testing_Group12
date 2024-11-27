from online_shopping_cart.user.user_authentication import UserAuthenticator, PasswordValidator
from online_shopping_cart.product.product import Product
from online_shopping_cart.checkout.shopping_cart import ShoppingCart
from online_shopping_cart.user.user_logout import logout
from pytest import fixture, mark, raises
import json
"""

IMPORTANT: This file requires pytest-mock to be installed: 'pip install pytest-mock'.
"""
#everything written in this file was done by Julius Amorim according to the instructions given in the assignment 1 task 1
class TestLogin:
    @fixture
    def mock_load_users(self, mocker):
        return mocker.patch("online_shopping_cart.user.user_data.UserDataManager.load_users")
    @fixture
    def mock_save_users(self, mocker):
        return mocker.patch("online_shopping_cart.user.user_data.UserDataManager.save_users")

    def get_data(self):
        with open("./files/users.json", "r") as file:
            data = json.load(file)
        return data
    
    def test_get_data(self):
        try:
            self.get_data()
            assert True is True
        except FileNotFoundError:
            assert True is False

    def test_valid_password(self):
        assert PasswordValidator.is_valid("passworD123!") == True
        assert PasswordValidator.is_valid("short") == False
        assert PasswordValidator.is_valid("nospeeChialChar123") == False
        assert PasswordValidator.is_valid("nocapitalleter?!!") == False
    
    
    def test_register_user(self, mock_load_users, mock_save_users):
        mock_users_data = self.get_data()
        mock_load_users.return_value = mock_users_data
        UserAuthenticator.register("new_user", "passworD123!", mock_load_users.return_value)
        mock_save_users.assert_called_once()
        assert any(user["username"] == "new_user" for user in mock_load_users.return_value)
        assert any(user["password"] == "passworD123!" for user in mock_load_users.return_value)

    @mark.parametrize("username, password", [
        (123, "Notaproblem23*"),        
        (3.14, "Notaproblem23*"),         
        (["user"], "Notaproblem23*"),   
        ("Ramanathan", 123456),          
        ("Ramanathan", 45.67),           
        ("Ramanathan", ["Pass123!"]),    
        ])
    def test_login_invalid(self, mock_load_users, username, password):
        mock_users_data = self.get_data()
        mock_load_users.return_value = mock_users_data

        with raises(Exception):
            UserAuthenticator.login(
                username=username,
                password=password,
                data=mock_users_data
        )
            
    @mark.parametrize("username, password", [
        ("Ramanathan", "Notaproblem23*"), 
        ("Samantha", "SecurePass123/^"),        
        ("Maximus", "StrongPwd!23"),  
        ("Aria", "SecretPas!21sphrase"),   
        ("Phoenix", "Firebir&^d987"), 
        ("Luna", "Moonlight#456"),       
        ("Rover", "Dog12@34"),     
        ("Felix", "Whisk&ers789"),  
        ("Zara", "Rai#nbow2022"),  
        ("Tiger", "Stripes5^67"),  
    ])
    def test_login_valid(self, username, password, mock_load_users):
        mock_users_data = self.get_data()
        mock_load_users.return_value = mock_users_data
        result = UserAuthenticator.login(
            username=username,
            password=password,
            data=mock_users_data
        )
        assert result is not None
        assert result["username"] == username
        assert "password" not in result

class TestLogout:
    @fixture
    def mock_input(self, mocker):
        return mocker.patch("online_shopping_cart.user.user_interface.UserInterface.get_user_input")
    
    @mark.parametrize("invalid_cart", [
        123,             
        4.5,              
        "yo",             
        ["Ramanathan"]
    ])
    def test_logout_invalid(self, invalid_cart):
        with raises(Exception):
            logout(invalid_cart)

    @mark.parametrize("valid_cart", [
        [Product("Apple", 2, 10)], 
        [Product("Banana", 1, 15)],
        [Product("Orange", 1.5, 8)],
        [Product("Grapes", 3, 5)],
        [Product("Strawberry", 4, 12)],
        [Product("Watermelon", 10, 1)],
        [Product("Carrot", 0.5, 20)],
        [Product("Broccoli", 1.5, 10)],
        [Product("Tomato", 1, 15)],
        [Product("Cucumber", 1, 12)],
    ])
    def test_logout_valid(self, valid_cart, mock_input):
        mock_input.return_value = "y"
        cart = ShoppingCart()
        for item in valid_cart:
            cart.add_item(item)

        result = logout(cart)
        assert result is True  
        assert not cart.is_empty()
        assert len(cart.retrieve_items()) == len(valid_cart)

    def test_logout_no(self, mock_input):
        cart = ShoppingCart()
        mock_input.return_value = "n"
        result = logout(cart)
        assert result is False
    
    def test_logout_yes(self, mock_input):
        cart = ShoppingCart()
        mock_input.return_value = "y"
        result = logout(cart)
        assert result is True