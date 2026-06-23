"""
Pytest test cases for calculator functions.
"""

from calculator import add


def test_add_positive_numbers() -> None:
    """
    Test addition of two positive numbers.
    """
    assert add(10, 5) == 15


def test_add_negative_numbers() -> None:
    """
    Test addition of two negative numbers.
    """
    assert add(-4, -6) == -10


def test_add_zero() -> None:
    """
    Test addition when one value is zero.
    """
    assert add(8, 0) == 8


def test_add_mixed_numbers() -> None:
    """
    Test addition of positive and negative numbers.
    """
    assert add(12, -5) == 7