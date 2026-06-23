"""
Examples demonstrating multiprocessing in Python.
"""

import multiprocessing
import os


def print_process(process_name: str) -> None:
    """
    to Print the process name along with its process ID.
    """
    print(f"{process_name} - Process ID: {os.getpid()}")


def calculate_square(number: int) -> None:
    """
    to Calculate and print the square of a number.
    """
    print(f"Square of {number}: {number * number}")


def main() -> None:
    """
    to Execute multiprocessing examples.
    """
    process_one = multiprocessing.Process(
        target=print_process,
        args=("Process-1",)
    )

    process_two = multiprocessing.Process(
        target=print_process,
        args=("Process-2",)
    )

    square_processes = []

    for number in [2, 4, 6, 8]:
        process = multiprocessing.Process(
            target=calculate_square,
            args=(number,)
        )
        square_processes.append(process)

    process_one.start()
    process_two.start()

    process_one.join()
    process_two.join()

    print("\nProcess ID demonstration completed.\n")

    for process in square_processes:
        process.start()

    for process in square_processes:
        process.join()

    print("\nSquare calculation completed.")


if __name__ == "__main__":
    main()