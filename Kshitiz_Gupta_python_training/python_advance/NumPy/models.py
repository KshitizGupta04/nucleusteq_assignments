"""
Assignment 1: NumPy Basics
"""

import numpy as np


class NumPy :
    """Perform basic NumPy operations."""

    def create_array(self):
        """Create and return a NumPy array."""
        return np.array([10, 20, 30, 40, 50])

    def show_statistics(self, numbers):
        """Display basic statistics."""
        print("Array:", numbers)
        print("Mean:", np.mean(numbers))
        print("Maximum:", np.max(numbers))
        print("Minimum:", np.min(numbers))
        print("Sum:", np.sum(numbers))

    def perform_operations(self):
        """Perform addition and multiplication of two arrays."""

        arr_1 = np.array([1, 2, 3])
        arr_2 = np.array([4, 5, 6])

        print("\nAddition:")
        print(arr_1 + arr_2)

        print("\nMultiplication:")
        print(arr_1 * arr_2)

    def create_matrix(self):
        """Create and display a 3 x 3 matrix."""

        matrix = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])

        print("\n3 x 3 Matrix:")
        print(matrix)


def main():
    """Driver function."""

    try:
        numpy_basics = NumPy()

        numbers = numpy_basics.create_array()
        numpy_basics.show_statistics(numbers)
        numpy_basics.perform_operations()
        numpy_basics.create_matrix()

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()