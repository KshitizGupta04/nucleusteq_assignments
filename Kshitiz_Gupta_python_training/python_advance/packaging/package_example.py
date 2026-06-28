"""
Example demonstrating how to import functions from another module.
"""

from utilities import find_square, greet


def main() -> None:
    """
    Demonstrate utility functions.
    """
    print(greet("Kshitiz"))
    print(f"Square of 8: {find_square(8)}")


if __name__ == "__main__":
    main()