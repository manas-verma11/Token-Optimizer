import pytest
from cost_calculator import calculate_input_cost


def test_default_price():
    assert calculate_input_cost(1000, 2.0) == 0.002

def test_one_million_tokens():
    assert calculate_input_cost(1_000_000, 2.0) == 2.0

def test_custom_price():
    assert calculate_input_cost(1000, 8.0) == 0.008

def test_negative_token_count():
    with pytest.raises(ValueError):
        calculate_input_cost(-1000, 2.0)

def test_negative_price():
    with pytest.raises(ValueError):
        calculate_input_cost(1000, -2.0)