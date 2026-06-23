"""
Program demonstrating the use of arithmetic operations.
"""

from arithmetic import add, divide, multiply, subtract


def main() -> None:
    """
    Demonstrate arithmetic operations.
    """
    first_number = 20
    second_number = 5

    print(f"Addition: {add(first_number, second_number)}")
    print(f"Subtraction: {subtract(first_number, second_number)}")
    print(f"Multiplication: {multiply(first_number, second_number)}")
    print(f"Division: {divide(first_number, second_number)}")


if __name__ == "__main__":
    main()