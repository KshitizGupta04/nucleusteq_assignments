"""
Examples demonstrating Python exception handling.
"""

FILE_NAME = "number.txt"


def handle_value_error() -> None:
    """
    Read an integer from the user and handle invalid input.
    """
    try:
        number = int(input("Enter an integer: "))
        print(f"You entered: {number}")
    except ValueError:
        print("Please enter a valid integer.")


def divide_numbers() -> None:
    """
    Divide two user-provided numbers.
    """
    try:
        first_number = float(input("Enter first number: "))
        second_number = float(input("Enter second number: "))

        result = first_number / second_number

    except ZeroDivisionError:
        print("Division by zero is not allowed.")

    except ValueError:
        print("Please enter numeric values.")

    else:
        print(f"Result: {result}")


def read_number_from_file() -> None:
    """
    Read a number from a file and print its square.
    """
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            number = int(file.read().strip())

    except FileNotFoundError:
        print(f"{FILE_NAME} not found.")

    except ValueError:
        print("File does not contain a valid integer.")

    else:
        print(f"Square: {number ** 2}")

    finally:
        print("File operation completed.")


def handle_multiple_exceptions() -> None:
    """
    Demonstrate handling multiple exceptions.
    """
    try:
        value = int(input("Enter a number: "))
        print(100 / value)

    except ValueError:
        print("Only integers are allowed.")

    except ZeroDivisionError:
        print("Cannot divide by zero.")


def catch_all_exceptions() -> None:
    """
    Catch any unexpected exception.
    """
    try:
        values = [10, 20]

        print(values[5])

    except Exception as error:
        print(f"Unexpected error: {error}")


def main() -> None:
    """
    Execute all examples.
    """
    handle_value_error()

    divide_numbers()

    read_number_from_file()

    handle_multiple_exceptions()

    catch_all_exceptions()


if __name__ == "__main__":
    main()