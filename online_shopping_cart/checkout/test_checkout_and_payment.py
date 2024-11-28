from online_shopping_cart.checkout.checkout_process import checkout_and_payment
import pytest


# Returns a dictionary containing invalid input types
@pytest.fixture
def invalid_input_type():
    return {"int": 1, "float": 0.5, "string": "notDict", "list": [1]}


# Returns user's login information
@pytest.fixture
def login_info():
    return {"username": "username", "password": "P@ssword", "wallet": 100.0}


@pytest.fixture
def global_products_stub1(mocker):
    product1 = mocker.Mock()
    product1.name = 'product1'
    product1.units = 1
    product2 = mocker.Mock()
    product2.name = 'product2'
    product2.units = 0
    return mocker.patch('online_shopping_cart.checkout.checkout_process.global_products', [product1, product2])


@pytest.fixture
def global_cart_stub1(mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.global_cart', mocker.Mock())


@pytest.fixture
def user_stub1(mocker):
    user = mocker.Mock()
    user.name = 'username'
    user.wallet = 100.0
    return mocker.patch('online_shopping_cart.checkout.checkout_process.User', return_value=user)


@pytest.fixture
def display_products_available_for_purchase_stub1(mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.display_products_available_for_purchase', return_value=None)


@pytest.fixture
def check_cart_stub1(mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.check_cart', return_value=True)


@pytest.fixture
def check_cart_stub2(mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.check_cart', return_value=False)


@pytest.fixture
def check_cart_stub3(mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.check_cart', side_effect=[False, True])


@pytest.fixture
def load_users_stub1(login_info, mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.UserDataManager.load_users', return_value=[login_info])


@pytest.fixture
def save_users_stub1(mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.UserDataManager.save_users', return_value=None)


@pytest.fixture
def logout_stub1(mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.logout', return_value=True)


@pytest.fixture
def logout_stub2(mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.logout', side_effect=[False, True])


@pytest.fixture
def input_stub1(mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.UserInterface.get_user_input', return_value='l')


@pytest.fixture
def input_stub2(mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.UserInterface.get_user_input', side_effect=['l', 'l'])


@pytest.fixture
def input_stub3(mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.UserInterface.get_user_input', side_effect=['1', 'l'])


@pytest.fixture
def input_stub4(mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.UserInterface.get_user_input', side_effect=['1', '1', 'l'])


@pytest.fixture
def input_stub5(mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.UserInterface.get_user_input', side_effect=['2', 'l'])


@pytest.fixture
def input_stub6(mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.UserInterface.get_user_input', side_effect=['2', '2', 'l'])


@pytest.fixture
def input_stub7(mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.UserInterface.get_user_input', side_effect=['1', '2', 'l'])


@pytest.fixture
def input_stub8(mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.UserInterface.get_user_input', side_effect=['2', '1', 'l'])


@pytest.fixture
def input_stub9(mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.UserInterface.get_user_input', side_effect=['c', 'l'])


@pytest.fixture
def input_stub10(mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.UserInterface.get_user_input', side_effect=['1', 'c', 'l'])


@pytest.fixture
def input_stub11(mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.UserInterface.get_user_input', side_effect=['1', '1', 'c', 'l'])


@pytest.fixture
def input_stub12(mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.UserInterface.get_user_input', side_effect=['1', 'c', '1', 'c', 'l'])


@pytest.fixture
def input_stub13(mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.UserInterface.get_user_input', side_effect=['d', 'l'])


@pytest.fixture
def input_stub14(mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.UserInterface.get_user_input', side_effect=['d', '1', 'c', 'l'])


@pytest.fixture
def input_stub15(mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.UserInterface.get_user_input', side_effect=['invalid', 'l'])


@pytest.fixture
def input_stub16(mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.UserInterface.get_user_input', side_effect=['0', 'l'])


@pytest.fixture
def input_stub17(mocker):
    return mocker.patch('online_shopping_cart.checkout.checkout_process.UserInterface.get_user_input', side_effect=['3', 'l'])


def test_int_input(invalid_input_type):
    # The checkout_and_payment function should throw a TypeError exception in case of invalid input type
    with pytest.raises(TypeError) as excinfo:
        checkout_and_payment(invalid_input_type['int'])
    assert "'int' object is not subscriptable" in str(excinfo.value)


def test_float_input(invalid_input_type):
    with pytest.raises(TypeError) as excinfo:
        checkout_and_payment(invalid_input_type['float'])
    assert "'float' object is not subscriptable" in str(excinfo.value)


def test_string_input(invalid_input_type):
    with pytest.raises(TypeError) as excinfo:
        checkout_and_payment(invalid_input_type['string'])
    assert "string indices must be integers, not 'str'" in str(excinfo.value)


def test_list_input(invalid_input_type):
    with pytest.raises(TypeError) as excinfo:
        checkout_and_payment(invalid_input_type['list'])
    assert 'list indices must be integers or slices, not str' in str(excinfo.value)


def test_EC1_TC1(login_info, global_products_stub1, global_cart_stub1, user_stub1, input_stub1, logout_stub1, capsys):
    with pytest.raises(SystemExit) as e:
        checkout_and_payment(login_info)
    assert e.value.code == 0
    # Assert that the logout function was called with the correct argument
    logout_stub1.assert_called_once_with(cart=global_cart_stub1)
    assert capsys.readouterr().out.strip() == ''


def test_EC1_TC2(login_info, global_products_stub1, global_cart_stub1, user_stub1, input_stub2, logout_stub2, mocker, capsys):
    with pytest.raises(SystemExit) as e:
        checkout_and_payment(login_info)
    assert e.value.code == 0
    # Assert that the logout function was called twice with the correct argument
    logout_stub2.assert_has_calls(2*[mocker.call(cart=global_cart_stub1)])
    assert capsys.readouterr().out.strip() == ''


def test_EC2_TC1(login_info, global_products_stub1, global_cart_stub1, user_stub1, input_stub3, logout_stub1, capsys):
    with pytest.raises(SystemExit) as e:
        checkout_and_payment(login_info)
    assert e.value.code == 0
    logout_stub1.assert_called_once_with(cart=global_cart_stub1)
    # Assert that the get_product_unit function was called once on the first product, i.e. the product that is in stock
    global_products_stub1[0].get_product_unit.assert_called_once()
    # Assert that the add_item function was called once with the correct argument
    global_cart_stub1.add_item.assert_called_once_with(product=global_products_stub1[0].get_product_unit.return_value)
    assert capsys.readouterr().out.strip() == f'{global_products_stub1[0].name} added to your cart.'


def test_EC2_TC2(login_info, global_products_stub1, global_cart_stub1, user_stub1, input_stub4, logout_stub1, mocker, capsys):
    with pytest.raises(SystemExit) as e:
        checkout_and_payment(login_info)
    assert e.value.code == 0
    logout_stub1.assert_called_once_with(cart=global_cart_stub1)
    # Assert that the get_product_unit function was called twice on the first product
    assert global_products_stub1[0].get_product_unit.call_count == 2
    # Assert that the add_item function was called twice with the correct argument
    assert global_cart_stub1.add_item.call_count == 2
    global_cart_stub1.add_item.assert_has_calls(2 * [mocker.call(product=global_products_stub1[0].get_product_unit.return_value)])
    assert capsys.readouterr().out.strip() == f'{global_products_stub1[0].name} added to your cart.\n{global_products_stub1[0].name} added to your cart.'


def test_EC2_TC3(login_info, global_products_stub1, global_cart_stub1, user_stub1, input_stub5, logout_stub1, capsys):
    with pytest.raises(SystemExit) as e:
        checkout_and_payment(login_info)
    assert e.value.code == 0
    logout_stub1.assert_called_once_with(cart=global_cart_stub1)
    # Assert that the get_product_unit function was not called on the second product, i.e. the product that is out of stock
    global_products_stub1[1].get_product_unit.assert_not_called()
    # Assert that the add_item function was not called
    global_cart_stub1.add_item.assert_not_called()
    assert capsys.readouterr().out.strip() == f'Sorry, {global_products_stub1[1].name} is out of stock.'


def test_EC2_TC4(login_info, global_products_stub1, global_cart_stub1, user_stub1, input_stub6, logout_stub1, capsys):
    with pytest.raises(SystemExit) as e:
        checkout_and_payment(login_info)
    assert e.value.code == 0
    logout_stub1.assert_called_once_with(cart=global_cart_stub1)
    global_products_stub1[1].get_product_unit.assert_not_called()
    global_cart_stub1.add_item.assert_not_called()
    assert capsys.readouterr().out.strip() == f'Sorry, {global_products_stub1[1].name} is out of stock.\nSorry, {global_products_stub1[1].name} is out of stock.'


def test_EC2_TC5(login_info, global_products_stub1, global_cart_stub1, user_stub1, input_stub7, logout_stub1, capsys):
    with pytest.raises(SystemExit) as e:
        checkout_and_payment(login_info)
    assert e.value.code == 0
    logout_stub1.assert_called_once_with(cart=global_cart_stub1)
    global_products_stub1[0].get_product_unit.assert_called_once()
    global_products_stub1[1].get_product_unit.assert_not_called()
    global_cart_stub1.add_item.assert_called_once_with(product=global_products_stub1[0].get_product_unit.return_value)
    assert capsys.readouterr().out.strip() == f'{global_products_stub1[0].name} added to your cart.\nSorry, {global_products_stub1[1].name} is out of stock.'


def test_EC2_TC6(login_info, global_products_stub1, global_cart_stub1, user_stub1, input_stub8, logout_stub1, capsys):
    with pytest.raises(SystemExit) as e:
        checkout_and_payment(login_info)
    assert e.value.code == 0
    logout_stub1.assert_called_once_with(cart=global_cart_stub1)
    global_products_stub1[0].get_product_unit.assert_called_once()
    global_products_stub1[1].get_product_unit.assert_not_called()
    global_cart_stub1.add_item.assert_called_once_with(product=global_products_stub1[0].get_product_unit.return_value)
    assert capsys.readouterr().out.strip() == f'Sorry, {global_products_stub1[1].name} is out of stock.\n{global_products_stub1[0].name} added to your cart.'


def test_EC3_TC1(login_info, global_products_stub1, global_cart_stub1, user_stub1, input_stub9, check_cart_stub1, load_users_stub1, save_users_stub1, logout_stub1, capsys):
    with pytest.raises(SystemExit) as e:
        checkout_and_payment(login_info)
    assert e.value.code == 0
    logout_stub1.assert_called_once_with(cart=global_cart_stub1)
    # Assert that the check_cart function was called with the correct arguments
    check_cart_stub1.assert_called_once_with(user=user_stub1.return_value, cart=global_cart_stub1)
    # Assert that the load_users function was called once
    load_users_stub1.assert_called_once()
    # Assert that the save_users function was called with the correct arguments
    save_users_stub1.assert_called_once_with(data=load_users_stub1.return_value)
    assert capsys.readouterr().out.strip() == ''


def test_EC3_TC2(login_info, global_products_stub1, global_cart_stub1, user_stub1, input_stub10, check_cart_stub1, load_users_stub1, save_users_stub1, logout_stub1, capsys):
    with pytest.raises(SystemExit) as e:
        checkout_and_payment(login_info)
    assert e.value.code == 0
    logout_stub1.assert_called_once_with(cart=global_cart_stub1)
    global_products_stub1[0].get_product_unit.assert_called_once()
    global_cart_stub1.add_item.assert_called_once_with(product=global_products_stub1[0].get_product_unit.return_value)
    check_cart_stub1.assert_called_once_with(user=user_stub1.return_value, cart=global_cart_stub1)
    load_users_stub1.assert_called_once()
    save_users_stub1.assert_called_once_with(data=load_users_stub1.return_value)
    assert capsys.readouterr().out.strip() == f'{global_products_stub1[0].name} added to your cart.'


def test_EC3_TC3(login_info, global_products_stub1, global_cart_stub1, user_stub1, input_stub11, check_cart_stub1, load_users_stub1, save_users_stub1, logout_stub1, mocker, capsys):
    with pytest.raises(SystemExit) as e:
        checkout_and_payment(login_info)
    assert e.value.code == 0
    logout_stub1.assert_called_once_with(cart=global_cart_stub1)
    assert global_products_stub1[0].get_product_unit.call_count == 2
    assert global_cart_stub1.add_item.call_count == 2
    global_cart_stub1.add_item.assert_has_calls(2 * [mocker.call(product=global_products_stub1[0].get_product_unit.return_value)])
    check_cart_stub1.assert_called_once_with(user=user_stub1.return_value, cart=global_cart_stub1)
    load_users_stub1.assert_called_once()
    save_users_stub1.assert_called_once_with(data=load_users_stub1.return_value)
    assert capsys.readouterr().out.strip() == f'{global_products_stub1[0].name} added to your cart.\n{global_products_stub1[0].name} added to your cart.'


def test_EC3_TC4(login_info, global_products_stub1, global_cart_stub1, user_stub1, input_stub9, check_cart_stub2, load_users_stub1, save_users_stub1, logout_stub1, capsys):
    with pytest.raises(SystemExit) as e:
        checkout_and_payment(login_info)
    assert e.value.code == 0
    logout_stub1.assert_called_once_with(cart=global_cart_stub1)
    # Assert that the check_cart function was called with the correct arguments
    check_cart_stub2.assert_called_once_with(user=user_stub1.return_value, cart=global_cart_stub1)
    # Assert that the load_users function was not called
    load_users_stub1.assert_not_called()
    # Assert that the save_users function was not called
    save_users_stub1.assert_not_called()
    assert capsys.readouterr().out.strip() == ''


def test_EC3_TC5(login_info, global_products_stub1, global_cart_stub1, user_stub1, input_stub10, check_cart_stub2, load_users_stub1, save_users_stub1, logout_stub1, capsys):
    with pytest.raises(SystemExit) as e:
        checkout_and_payment(login_info)
    assert e.value.code == 0
    logout_stub1.assert_called_once_with(cart=global_cart_stub1)
    global_products_stub1[0].get_product_unit.assert_called_once()
    global_cart_stub1.add_item.assert_called_once_with(product=global_products_stub1[0].get_product_unit.return_value)
    check_cart_stub2.assert_called_once_with(user=user_stub1.return_value, cart=global_cart_stub1)
    load_users_stub1.assert_not_called()
    save_users_stub1.assert_not_called()
    assert capsys.readouterr().out.strip() == f'{global_products_stub1[0].name} added to your cart.'


def test_EC3_TC6(login_info, global_products_stub1, global_cart_stub1, user_stub1, input_stub11, check_cart_stub2, load_users_stub1, save_users_stub1, logout_stub1, mocker, capsys):
    with pytest.raises(SystemExit) as e:
        checkout_and_payment(login_info)
    assert e.value.code == 0
    logout_stub1.assert_called_once_with(cart=global_cart_stub1)
    assert global_products_stub1[0].get_product_unit.call_count == 2
    assert global_cart_stub1.add_item.call_count == 2
    global_cart_stub1.add_item.assert_has_calls(2 * [mocker.call(product=global_products_stub1[0].get_product_unit.return_value)])
    check_cart_stub2.assert_called_once_with(user=user_stub1.return_value, cart=global_cart_stub1)
    load_users_stub1.assert_not_called()
    save_users_stub1.assert_not_called()
    assert capsys.readouterr().out.strip() == f'{global_products_stub1[0].name} added to your cart.\n{global_products_stub1[0].name} added to your cart.'


def test_EC3_TC7(login_info, global_products_stub1, global_cart_stub1, user_stub1, input_stub12, check_cart_stub3, load_users_stub1, save_users_stub1, logout_stub1, mocker, capsys):
    with pytest.raises(SystemExit) as e:
        checkout_and_payment(login_info)
    assert e.value.code == 0
    logout_stub1.assert_called_once_with(cart=global_cart_stub1)
    assert global_products_stub1[0].get_product_unit.call_count == 2
    assert global_cart_stub1.add_item.call_count == 2
    global_cart_stub1.add_item.assert_has_calls(2 * [mocker.call(product=global_products_stub1[0].get_product_unit.return_value)])
    assert check_cart_stub3.call_count == 2
    check_cart_stub3.assert_has_calls(2 *[mocker.call(user=user_stub1.return_value, cart=global_cart_stub1)])
    load_users_stub1.assert_called_once()
    save_users_stub1.assert_called_once_with(data=load_users_stub1.return_value)
    assert capsys.readouterr().out.strip() == f'{global_products_stub1[0].name} added to your cart.\n{global_products_stub1[0].name} added to your cart.'


def test_EC4_TC1(login_info, global_products_stub1, global_cart_stub1, user_stub1, input_stub13, display_products_available_for_purchase_stub1, logout_stub1, capsys):
    with pytest.raises(SystemExit) as e:
        checkout_and_payment(login_info)
    assert e.value.code == 0
    logout_stub1.assert_called_once_with(cart=global_cart_stub1)
    display_products_available_for_purchase_stub1.assert_called_once()
    assert capsys.readouterr().out.strip() == ''


def test_EC4_TC2(login_info, global_products_stub1, global_cart_stub1, user_stub1, input_stub14, display_products_available_for_purchase_stub1, check_cart_stub1, load_users_stub1, save_users_stub1, logout_stub1, capsys):
    with pytest.raises(SystemExit) as e:
        checkout_and_payment(login_info)
    assert e.value.code == 0
    logout_stub1.assert_called_once_with(cart=global_cart_stub1)
    display_products_available_for_purchase_stub1.assert_called_once()
    global_products_stub1[0].get_product_unit.assert_called_once()
    global_cart_stub1.add_item.assert_called_once_with(product=global_products_stub1[0].get_product_unit.return_value)
    check_cart_stub1.assert_called_once_with(user=user_stub1.return_value, cart=global_cart_stub1)
    load_users_stub1.assert_called_once()
    save_users_stub1.assert_called_once_with(data=load_users_stub1.return_value)
    assert capsys.readouterr().out.strip() == f'{global_products_stub1[0].name} added to your cart.'


def test_EC5_TC1(login_info, global_products_stub1, global_cart_stub1, user_stub1, input_stub15, logout_stub1, capsys):
    with pytest.raises(SystemExit) as e:
        checkout_and_payment(login_info)
    assert e.value.code == 0
    logout_stub1.assert_called_once_with(cart=global_cart_stub1)
    assert capsys.readouterr().out.strip() == 'Invalid input. Please try again.'


def test_EC5_TC2(login_info, global_products_stub1, global_cart_stub1, user_stub1, input_stub16, logout_stub1, capsys):
    with pytest.raises(SystemExit) as e:
        checkout_and_payment(login_info)
    assert e.value.code == 0
    logout_stub1.assert_called_once_with(cart=global_cart_stub1)
    assert capsys.readouterr().out.strip() == 'Invalid input. Please try again.'


def test_EC5_TC3(login_info, global_products_stub1, global_cart_stub1, user_stub1, input_stub17, logout_stub1, capsys):
    with pytest.raises(SystemExit) as e:
        checkout_and_payment(login_info)
    assert e.value.code == 0
    logout_stub1.assert_called_once_with(cart=global_cart_stub1)
    assert capsys.readouterr().out.strip() == 'Invalid input. Please try again.'