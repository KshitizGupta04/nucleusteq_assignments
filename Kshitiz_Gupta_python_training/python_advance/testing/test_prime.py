"""
Pytest test cases for prime number checking.
"""

from prime import is_prime


def test_prime_number() -> None:
    """
    to Verify a prime number.
    """
    assert is_prime(17)


def test_non_prime_number() -> None:
    """
    to Verify a non-prime number.
    """
    assert not is_prime(15)


def test_zero() -> None:
    """
    to verify Zero should not be prime.
    """
    assert not is_prime(0)


def test_one() -> None:
    """
    to show One should not be prime.
    """
    assert not is_prime(1)


def test_negative_number() -> None:
    """
    to check Negative numbers are not prime.
    """
    assert not is_prime(-9)