"""
Example demonstrating how to import a module.
"""

from utilities import greet, find_square


def main() -> None:
    """
    Demonstrate utility functions.
    """
    print(greet("Kshitiz"))
    print(f"Square: {find_square(8)}")


if __name__ == "__main__":
    main()