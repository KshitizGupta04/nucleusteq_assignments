"""
Utility functions used for pytest examples.
"""


def add(first_number: int, second_number: int) -> int:
    """
    Return the sum of two numbers.
    """
    return first_number + second_number


def main() -> None:
    """
    Demonstrate the add function.
    """
    result = add(15, 25)
    print(f"Sum: {result}")


if __name__ == "__main__":
    main()