"""
Examples demonstrating threading in Python.
"""

import threading
import time


START_NUMBER = 1
END_NUMBER = 5


def print_numbers(thread_name: str) -> None:
    """
    to Print numbers from START_NUMBER to END_NUMBER.
    """
    for number in range(START_NUMBER, END_NUMBER + 1):
        print(f"{thread_name}: {number}")
        time.sleep(0.2)


def calculate_sum() -> None:
    """
    to Calculate the sum of numbers from 1 to 100.
    """
    total = sum(range(1, 101))
    print(f"Sum from 1 to 100: {total}")


def download_file(file_name: str) -> None:
    """
    to Simulate downloading a file.
    """
    print(f"Downloading {file_name}...")
    time.sleep(2)
    print(f"{file_name} downloaded.")


def main() -> None:
    """
    to Execute threading examples.
    """
    thread_one = threading.Thread(
        target=print_numbers,
        args=("Thread-1",)
    )

    thread_two = threading.Thread(
        target=print_numbers,
        args=("Thread-2",)
    )

    sum_thread = threading.Thread(target=calculate_sum)

    download_threads = [
        threading.Thread(
            target=download_file,
            args=(f"File-{index}.txt",)
        )
        for index in range(1, 4)
    ]

    thread_one.start()
    thread_two.start()

    thread_one.join()
    thread_two.join()

    print("\nNumber printing completed.\n")

    sum_thread.start()
    sum_thread.join()

    print("\nDownloading Files\n")

    for thread in download_threads:
        thread.start()

    for thread in download_threads:
        thread.join()

    print("\nAll downloads completed.")


if __name__ == "__main__":
    main()