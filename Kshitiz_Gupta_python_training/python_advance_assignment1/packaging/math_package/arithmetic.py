"""
Basic arithmetic operations.
"""


def add(first_number: float, second_number: float) -> float:
    """
    Return the sum of two numbers.
    """
    return first_number + second_number


def subtract(first_number: float, second_number: float) -> float:
    """
    Return the difference between two numbers.
    """
    return first_number - second_number


def multiply(first_number: float, second_number: float) -> float:
    """
    Return the product of two numbers.
    """
    return first_number * second_number


def divide(first_number: float, second_number: float) -> float:
    """
    Return the division of two numbers.
    """
    if second_number == 0:
        raise ZeroDivisionError("Division by zero is not allowed.")

    return first_number / second_number