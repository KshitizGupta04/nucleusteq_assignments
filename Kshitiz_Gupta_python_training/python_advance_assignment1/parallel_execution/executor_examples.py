"""
Examples demonstrating ThreadPoolExecutor and ProcessPoolExecutor.
"""

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import time


def calculate_square(number: int) -> int:
    """
    to Return the square of a number.
    """
    time.sleep(1)
    return number * number


def calculate_cube(number: int) -> int:
    """
    to Return the cube of a number.
    """
    time.sleep(1)
    return number * number * number


def thread_pool_example() -> None:
    """
    to Execute tasks using ThreadPoolExecutor.
    """
    numbers = [1, 2, 3, 4, 5]

    print("ThreadPoolExecutor Results")

    with ThreadPoolExecutor(max_workers=3) as executor:
        results = executor.map(calculate_square, numbers)

        for value in results:
            print(value)


def process_pool_example() -> None:
    """
    ro Execute tasks using ProcessPoolExecutor.
    """
    numbers = [1, 2, 3, 4, 5]

    print("\nProcessPoolExecutor Results")

    with ProcessPoolExecutor(max_workers=3) as executor:
        results = executor.map(calculate_cube, numbers)

        for value in results:
            print(value)


def main() -> None:
    """
    ro Execute executor examples.
    """
    thread_pool_example()

    process_pool_example()


if __name__ == "__main__":
    main()