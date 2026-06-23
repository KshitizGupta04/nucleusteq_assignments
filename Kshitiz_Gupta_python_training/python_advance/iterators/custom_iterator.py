"""
Custom iterator example.
This module demonstrates how to create an iterator class that returns numbers from 1 to a given limit.
"""


class NumberIterator:
    """
    Iterator that returns numbers from 1 to the specified limit.
    """

    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.current = 1

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self.current > self.limit:
            raise StopIteration

        number = self.current
        self.current += 1
        return number


def simple_generator(limit: int):
    """
    Generator that yields numbers from 1 to the specified limit.
    """
    for number in range(1, limit + 1):
        yield number


def main() -> None:
    """
    Demonstrate iterator and generator usage.
    """
    print("Custom Iterator")

    iterator = NumberIterator(5)

    for value in iterator:
        print(value)

    print("\nGenerator")

    for value in simple_generator(5):
        print(value)

    print("\nDifference")
    print("Iterator: Requires __iter__() and __next__() methods.")
    print("Generator: Uses yield and creates an iterator automatically.")


if __name__ == "__main__":
    main()