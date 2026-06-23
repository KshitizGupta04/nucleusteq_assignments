"""
Examples of raising built-in and custom exceptions.
"""

MINIMUM_AGE = 18


class AgeException(Exception):
    """
    to provide exception when age is below the minimum required value.
    """


def validate_positive_number(number: int) -> None:
    """
    to provide exception ValueError if the number is negative.
    """
    if number < 0:
        raise ValueError("Negative numbers are not allowed.")


def validate_age(age: int) -> None:
    """
    to Validate age using a custom exception.
    """
    if age < MINIMUM_AGE:
        raise AgeException(
            f"Age should be at least {MINIMUM_AGE}."
        )


def main() -> None:
    """
    to Demonstrate custom exceptions.
    """
    try:
        validate_positive_number(-5)

    except ValueError as error:
        print(error)

    try:
        validate_age(16)

    except AgeException as error:
        print(error)


if __name__ == "__main__":
    main()