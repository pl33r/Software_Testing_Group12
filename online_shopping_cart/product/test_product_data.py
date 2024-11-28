
from online_shopping_cart.product.product_data import get_products
from unittest.mock import mock_open,patch
import pytest


#Test cases for invalid input type(int,float,string,list)


def test_get_product_invalid_input_int():
    with pytest.raises(TypeError, match="File name must be a string"):
        get_products(1)

def test_get_product_invalid_input_float():
    with pytest.raises(TypeError):
        get_products(55.8)

def test_get_product_invalid_input_string():
    with pytest.raises(FileNotFoundError):
        get_products("abc.csv")


def test_get_product_invalid_input_lists():
    with pytest.raises(TypeError):
        get_products(["abc.csv","def.csv"])

#Test case for checking the csv file is valid
def test_get_product_valid_file():
    products = get_products('./files/products.csv')
    assert len(products) == 71
    assert products[0].name == 'Apple'
    assert products[0].price == 2
    assert products[0].units == 10
    assert products[1].name == 'Banana'
    assert products[1].price == 1
    assert products[1].units == 15
    assert products[-1].name == 'Backpack'
    assert products[-1].price == 15
    assert products[-1].units == 1

#Test case for empty csv file
def test_get_product_valid_empty_csv_file():
    empty_csv = ""
    mock_file = mock_open(read_data=empty_csv)
    with patch('builtins.open', mock_file):
        products = get_products('mocked_empty.csv')
    assert len(products) == 0

#Test case for malformed csv files
def test_get_product_malformed_valid_csv_file1():
    invalid_csv="Apple,2,20\nBanana,1\nOrange,2,13"

    mock_file = mock_open(read_data=invalid_csv)
    with patch('builtins.open', mock_file):
        with pytest.raises(KeyError):
            get_products("mocked_invalid.csv")


def test_get_product_malformed_valid_csv_file2():
    invalid_csv="Apple,2,20\nBanana,1\nOrange,2,13"

    mock_file = mock_open(read_data=invalid_csv)
    with patch('builtins.open', mock_file):
        with pytest.raises(KeyError):
            get_products("mocked_invalid.csv")

def test_get_product_malformed_valid_csv_file3():
    invalid_csv="Apple,,20\nBanana,1,3\n,2,13"

    mock_file = mock_open(read_data=invalid_csv)
    with patch('builtins.open', mock_file):
        with pytest.raises(KeyError):
            get_products("mocked_invalid.csv")

#Test case for incorrect data types
def test_get_product_incorrect_data_type():
    invalid_csv = "Apple,three,30\nBanana,1,thirty\nOrange,2,13"

    mock_file = mock_open(read_data=invalid_csv)
    with patch('builtins.open', mock_file):
        with pytest.raises(KeyError):
            get_products("mocked.csv")
#Test case for special characters in product name
def test_get_product_special_characters():

    spcial_csv = "Product,Price,Units\n@pple,10,5\nB@n@n@,3,18"
    mock_file =  mock_open(read_data=spcial_csv)
    with patch('builtins.open', mock_file):
        products = get_products("prd.csv")
        assert len(products) == 2
        assert products[0].name == "@pple"
        assert products[1].name == "B@n@n@"

#Test case for white space
def test_get_products_white_space():
    sample_csv="Product,Price,Units\n  Apple  ,  2,  10  \n  Banana   ,4,  19  "
    mock_file = mock_open(read_data=sample_csv)
    with patch('builtins.open', mock_file):
        products = get_products("mocked.csv")
        assert len(products) == 2
        assert products[0].name.strip() == "Apple"
        assert products[1].name.strip() == "Banana"
#Test case for case sensitive
def test_get_products_case_sensitive():
    sample_csv="Product,Price,Units\napple,2,10\nbananA,4,19"
    mock_file = mock_open(read_data=sample_csv)
    with patch('builtins.open', mock_file):
        products = get_products("mocked.csv")
        assert len(products) == 2
        assert products[0].name.strip() == "apple"
        assert products[1].name.strip() == "bananA"
#Test case for extra fields in the csv
def test_get_products_extra_fields():
    valid_csv= "Product,Price,Units,Type\napple,2,10,Fruit\nbanana,4,19,Fruit"
    mock_file = mock_open(read_data=valid_csv)
    with patch('builtins.open', mock_file):
        products = get_products("mocked.csv")
        assert len(products) == 2
        assert products[0].name== "apple"











