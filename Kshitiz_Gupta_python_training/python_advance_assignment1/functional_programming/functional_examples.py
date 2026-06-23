"""
Examples demonstrating functional programming concepts in Python.
"""

from functools import reduce


def square(number: int) -> int:
    """
    Return the square of a number.
    """
    return number * number


def multiply(first: int, second: int) -> int:
    """
    Return the product of two numbers.
    """
    return first * second


def main() -> None:
    """
    Demonstrate lambda, map, filter and reduce.
    """
    numbers = [1, 2, 3, 4, 5, 6]

    square_lambda = lambda value: value * value

    print("Square using lambda:")
    print(square_lambda(7))

    squared_numbers = list(map(square, numbers))
    print("\nSquares using map:")
    print(squared_numbers)

    even_numbers = list(filter(lambda value: value % 2 == 0, numbers))
    print("\nEven numbers using filter:")
    print(even_numbers)

    product = reduce(multiply, numbers)
    print("\nProduct using reduce:")
    print(product)

    doubled_numbers = list(map(lambda value: value * 2, numbers))
    print("\nLoop converted to functional style:")
    print(doubled_numbers)


if __name__ == "__main__":
    main()