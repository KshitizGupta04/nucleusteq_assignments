import base64

from pathlib import (
    Path
)

import pytest

from cryptography.hazmat.primitives import (
    hashes,
    serialization
)

from cryptography.hazmat.primitives.asymmetric import (
    padding
)

from fastapi.testclient import (
    TestClient
)

from app.core.database import (
    db
)

from app.core.security import (
    hash_password
)

from main import (
    app
)


BASE_DIR = Path(
    __file__
).resolve().parents[1]


PUBLIC_KEY_PATH = (
    BASE_DIR
    / "keys"
    / "public_key.pem"
)


ADMIN_USERNAME = "admin"

ADMIN_EMAIL = "admin@gmail.com"

ADMIN_PASSWORD = "Admin@123"


TEST_COLLECTIONS = [
    "attempts",
    "results",
    "questions",
    "quizzes",
    "categories",
]


def encrypt_password(
    password: str
) -> str:

    with open(
        PUBLIC_KEY_PATH,
        "rb"
    ) as key_file:

        public_key = (
            serialization.load_pem_public_key(
                key_file.read()
            )
        )

    encrypted_password = (
        public_key.encrypt(
            password.encode(
                "utf-8"
            ),
            padding.OAEP(
                mgf=padding.MGF1(
                    algorithm=hashes.SHA256()
                ),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    )

    return base64.b64encode(
        encrypted_password
    ).decode(
        "utf-8"
    )


@pytest.fixture(
    scope="session"
)
def password_encryptor():

    return encrypt_password


def ensure_admin_exists():

    existing_admin = db[
        "users"
    ].find_one(
        {
            "username": ADMIN_USERNAME
        }
    )

    if existing_admin:

        return

    db["users"].insert_one(
        {
            "username": ADMIN_USERNAME,
            "email": ADMIN_EMAIL,
            "password": hash_password(
                ADMIN_PASSWORD
            ),
            "role": "admin"
        }
    )


def cleanup_test_data():

    for collection_name in TEST_COLLECTIONS:

        db[
            collection_name
        ].delete_many({})

    db["users"].delete_many(
        {
            "role": "student"
        }
    )


@pytest.fixture(
    scope="session",
    autouse=True
)
def setup_admin():

    ensure_admin_exists()

    yield


@pytest.fixture(
    scope="function",
    autouse=True
)
def clean_database_between_tests():

    cleanup_test_data()

    yield

    cleanup_test_data()


@pytest.fixture(
    scope="session"
)
def client():

    with TestClient(
        app
    ) as test_client:

        yield test_client


@pytest.fixture(
    scope="session"
)
def admin_token(
    client
):

    ensure_admin_exists()

    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": ADMIN_USERNAME,
            "password": encrypt_password(
                ADMIN_PASSWORD
            )
        }
    )

    assert response.status_code == 200, (
        f"Admin login failed: "
        f"{response.status_code} - "
        f"{response.text}"
    )

    return response.json()[
        "access_token"
    ]


@pytest.fixture(
    scope="session"
)
def admin_headers(
    admin_token
):

    return {
        "Authorization": (
            f"Bearer {admin_token}"
        )
    }


@pytest.fixture(
    scope="function"
)
def student_credentials():

    return {
        "username": (
            "test_student_category"
        ),
        "email": (
            "test_student_category"
            "@gmail.com"
        ),
        "password": "Student@123"
    }


@pytest.fixture(
    scope="function"
)
def student_token(
    client,
    student_credentials
):

    username = (
        student_credentials[
            "username"
        ]
    )

    email = (
        student_credentials[
            "email"
        ]
    )

    password = (
        student_credentials[
            "password"
        ]
    )

    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": email,
            "password": encrypt_password(
                password
            )
        }
    )

    assert register_response.status_code in (
        200,
        201
    ), (
        f"Student registration failed: "
        f"{register_response.status_code} - "
        f"{register_response.text}"
    )

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "username": username,
            "password": encrypt_password(
                password
            )
        }
    )

    assert login_response.status_code == 200, (
        f"Student login failed: "
        f"{login_response.status_code} - "
        f"{login_response.text}"
    )

    return login_response.json()[
        "access_token"
    ]


@pytest.fixture(
    scope="function"
)
def student_headers(
    student_token
):

    return {
        "Authorization": (
            f"Bearer {student_token}"
        )
    }