"""
Examples demonstrating the use of regular expressions.
"""

import re


EMAIL_PATTERN = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
MOBILE_PATTERN = r"^[6-9]\d{9}$"
ALPHABET_PATTERN = r"^[A-Za-z]+$"


def extract_numbers(text: str) -> list[str]:
    """
    Extract all numbers from a string.
    """
    return re.findall(r"\d+", text)


def validate_email(email: str) -> bool:
    """
    Validate an email address.
    """
    return re.fullmatch(EMAIL_PATTERN, email) is not None


def validate_mobile(number: str) -> bool:
    """
    Validate a 10-digit mobile number.
    """
    return re.fullmatch(MOBILE_PATTERN, number) is not None


def search_word(sentence: str, word: str) -> bool:
    """
    Check whether a word exists in a sentence.
    """
    return re.search(rf"\b{re.escape(word)}\b", sentence) is not None


def capital_words(sentence: str) -> list[str]:
    """
    Return all words starting with a capital letter.
    """
    return re.findall(r"\b[A-Z][a-zA-Z]*\b", sentence)


def remove_extra_spaces(text: str) -> str:
    """
    Replace multiple spaces with a single space.
    """
    return re.sub(r"\s+", " ", text).strip()


def contains_only_alphabets(text: str) -> bool:
    """
    Check whether the string contains only alphabets.
    """
    return re.fullmatch(ALPHABET_PATTERN, text) is not None


def main() -> None:
    """
    Demonstrate regex examples.
    """
    sample = "Kshitiz bought 12 books for 4500 rupees."

    print("Numbers:")
    print(extract_numbers(sample))

    print("\nEmail Validation:")
    print(validate_email("kshitiz@gmail.com"))

    print("\nMobile Validation:")
    print(validate_mobile("9876543210"))

    print("\nSearch Word:")
    print(search_word(sample, "books"))

    print("\nCapitalized Words:")
    print(capital_words("Kshitiz and Kunjesh visited Indore and Khargone."))

    print("\nRemove Extra Spaces:")
    print(remove_extra_spaces("Python     is      awesome"))

    print("\nAlphabet Check:")
    print(contains_only_alphabets("isAlphhabet"))


if __name__ == "__main__":
    main()