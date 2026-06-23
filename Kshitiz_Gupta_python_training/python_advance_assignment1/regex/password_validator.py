"""
Validate passwords using regular expressions.
"""

import re

MINIMUM_LENGTH = 8

PASSWORD_PATTERN = (
    rf"^(?=.*[A-Za-z])"
    rf"(?=.*\d)"
    rf"(?=.*[@$!%*?&])"
    rf"[A-Za-z\d@$!%*?&]{{{MINIMUM_LENGTH},}}$"
)


def is_valid_password(password: str) -> bool:
    """
    Check whether a password satisfies the required rules.

    Rules:
    - Minimum 8 characters
    - At least one alphabet
    - At least one digit
    - At least one special character
    """
    return re.fullmatch(PASSWORD_PATTERN, password) is not None


def main() -> None:
    """
    Read a password from the user and validate it.
    """
    password = input("Enter password: ")

    if is_valid_password(password):
        print("Password is valid.")
    else:
        print("Password is invalid.")
        print("Password must:")
        print(f"- Contain at least {MINIMUM_LENGTH} characters")
        print("- Include at least one alphabet")
        print("- Include at least one digit")
        print("- Include at least one special character (@$!%*?&)")


if __name__ == "__main__":
    main()