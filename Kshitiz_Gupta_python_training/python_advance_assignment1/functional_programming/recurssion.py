"""
Examples of recursive functions.
"""


def factorial(number: int) -> int:
    """
    to Return the factorial of a number.
    """
    if number < 0:
        raise ValueError("Factorial is not defined for negative numbers.")

    if number in (0, 1):
        return 1

    return number * factorial(number - 1)


def fibonacci(position: int) -> int:
    """
    to Return the Fibonacci number at the given position.
    """
    if position < 0:
        raise ValueError("Position cannot be negative.")

    if position <= 1:
        return position

    return fibonacci(position - 1) + fibonacci(position - 2)


def main() -> None:
    """
    to Demonstrate recursive functions.
    """
    value = 5

    print(f"Factorial of {value}: {factorial(value)}")

    print("\nFirst 10 Fibonacci numbers:")

    for index in range(10):
        print(fibonacci(index), end=" ")

    print()


if __name__ == "__main__":
    main()