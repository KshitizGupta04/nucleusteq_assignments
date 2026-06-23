"""
Examples demonstrating the use of Python generators.
"""


def square_numbers(limit: int):
    """
    to get square numbers from 1 to the given limit.
    """
    for number in range(1, limit + 1):
        yield number * number


def fibonacci(limit: int):
    """
    to get Fibonacci numbers up to the given count.
    """
    first, second = 0, 1

    for _ in range(limit):
        yield first
        first, second = second, first + second


def large_dataset(limit: int):
    """
    Simulate processing a large dataset without storing all values in memory.
    """
    for value in range(1, limit + 1):
        yield value


def main() -> None:
    """
    Run generator examples.
    """
    print("Square Numbers")
    for value in square_numbers(5):
        print(value)

    print("\nFibonacci Series")
    for value in fibonacci(10):
        print(value)

    print("\nEven Numbers (Generator Expression)")
    even_numbers = (number for number in range(1, 51) if number % 2 == 0)

    for number in even_numbers:
        print(number, end=" ")

    print("\n\nProcessing Large Dataset")

    total = 0
    for number in large_dataset(100000):
        total += number

    print(f"Sum: {total}")

    print("\nUsing range()")

    for value in range(1, 6):
        print(value)


if __name__ == "__main__":
    main()