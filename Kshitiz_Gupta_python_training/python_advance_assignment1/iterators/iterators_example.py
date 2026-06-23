"""
Examples demonstrating the use of Python iterators.
"""


def print_list_using_iterator(items: list[int]) -> None:
    """
    to Print all elements of a list using an iterator
    """
    iterator = iter(items)

    while True:
        try:
            print(next(iterator))
        except StopIteration:
            break


def main() -> None:
    """
    to Execute iterator examples.
    """
    numbers = [10, 20, 30, 40, 50]

    print("List elements using iterator:")
    print_list_using_iterator(numbers)


if __name__ == "__main__":
    main()