import base64

from pathlib import Path

from cryptography.hazmat.primitives import (
    hashes,
    serialization
)

from cryptography.hazmat.primitives.asymmetric import (
    padding
)


BASE_DIR = Path(__file__).resolve().parents[2]

PRIVATE_KEY_PATH = (
    BASE_DIR
    / "keys"
    / "private_key.pem"
)


def load_private_key():

    with open(
        PRIVATE_KEY_PATH,
        "rb"
    ) as key_file:

        private_key = (
            serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )
        )

    return private_key


def decrypt_password(
    encrypted_password: str
) -> str:

    private_key = load_private_key()

    encrypted_bytes = base64.b64decode(
        encrypted_password
    )

    decrypted_bytes = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted_bytes.decode(
        "utf-8"
    )

import re


def validate_password_strength(
    password: str
) -> str:

    if len(password) < 8:

        raise ValueError(
            "Password must be at least 8 characters."
        )

    if len(password) > 32:

        raise ValueError(
            "Password must be at most 32 characters."
        )

    if not re.search(
        r"[A-Z]",
        password
    ):

        raise ValueError(
            "Password must contain at least one uppercase letter."
        )

    if not re.search(
        r"[a-z]",
        password
    ):

        raise ValueError(
            "Password must contain at least one lowercase letter."
        )

    if not re.search(
        r"\d",
        password
    ):

        raise ValueError(
            "Password must contain at least one digit."
        )

    if not re.search(
        r"[!@#$%^&*()_\-+=]",
        password
    ):

        raise ValueError(
            "Password must contain at least one special character."
        )

    return password