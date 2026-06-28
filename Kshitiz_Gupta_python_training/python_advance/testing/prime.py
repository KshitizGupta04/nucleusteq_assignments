"""
Utility functions for checking prime numbers.
"""


def is_prime(number: int) -> bool:
    """
    to Return True if the given number is prime.
    """
    if number < 2:
        return False

    divisor = 2

    while divisor * divisor <= number:
        if number % divisor == 0:
            return False

        divisor += 1

    return True


def main() -> None:
    """
    to Demonstrate the prime checking function.
    """
    number = 17

    if is_prime(number):
        print(f"{number} is a prime number.")
    else:
        print(f"{number} is not a prime number.")


if __name__ == "__main__":
    main()