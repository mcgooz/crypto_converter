import pytest
from project import (input_check, input_strip, is_float, crypto2fiat, fiat2crypto)
from unittest.mock import patch

def test_input_check():
    with patch("project.crypto_menu.get", return_value="BTC") as mock_get:
        assert input_check("", "") == "empty"
        assert input_check("10", "") == "c2f"
        assert input_check("", "10") == "f2c"
        assert input_check("10", "10") == "clear"
        assert input_check("cat", "") == "invalid"
        assert input_check("", "dog") == "invalid"

def test_input_strip():
    assert input_strip("€1,234.56") == "1234.56"
    assert input_strip("1,234,567") == "1234567"
    assert input_strip("ETH 1,200") == "1200"
    assert input_strip("2,123.01 BTC") == "2123.01"

def test_is_float():
    assert is_float("1,234.56") == True
    assert is_float("€1,234.56EUR") == True
    assert is_float("BTC0.5") == True
    assert is_float("cat") == False
    assert is_float("$$$") == False

def test_crypto2fiat():
    with patch("project.crypto_price", return_value=100) as mock_get:
        assert crypto2fiat("2") == 200
        assert crypto2fiat("0.5") == 50

def test_fiat2crypto():
    with patch("project.crypto_price", return_value=100) as mock_get:
        assert fiat2crypto("2") == 0.02
        assert fiat2crypto("0.5") == 0.005