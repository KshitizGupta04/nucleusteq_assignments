"""
Examples demonstrating debugging using pdb.
"""

import pdb


def calculate_total(numbers: list[int]) -> int:
    """
    Calculate the total of all numbers.

    This function intentionally contains a logical bug
    for debugging practice.
    """
    total = 1  # Intentional bug is that it should start from 0 instead of 1

    for number in numbers:
        pdb.set_trace()
        total += number

    return total


def main() -> None:
    """
    Execute the debugging example.
    """
    values = [10, 20, 30]

    result = calculate_total(values)

    print(f"Total: {result}")


if __name__ == "__main__":
    main()