import base64
import uuid

from datetime import (
    datetime,
    timedelta,
    timezone
)

from pathlib import Path

from cryptography.hazmat.primitives import (
    hashes,
    serialization
)

from cryptography.hazmat.primitives.asymmetric import (
    padding
)

from jose import jwt

from app.core.config import settings


AUTH_URL = "/api/v1/auth"


BASE_DIR = Path(
    __file__
).resolve().parents[2]


PUBLIC_KEY_PATH = (
    BASE_DIR
    / "keys"
    / "public_key.pem"
)


# TEST HELPERS
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

    encrypted_bytes = public_key.encrypt(
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

    return base64.b64encode(
        encrypted_bytes
    ).decode(
        "utf-8"
    )


def create_student(
    client,
    username=None,
    email=None,
    password="Student@123"
):

    unique = uuid.uuid4().hex[:8]

    student_username = (
        username
        or f"student_{unique}"
    )

    student_email = (
        email
        or f"{unique}@gmail.com"
    )

    response = client.post(
        f"{AUTH_URL}/register",
        json={
            "username": student_username,
            "email": student_email,
            "password": encrypt_password(
                password
            )
        }
    )

    return (
        response,
        student_username,
        student_email,
        password
    )


def login_user(
    client,
    username,
    password
):

    return client.post(
        f"{AUTH_URL}/login",
        json={
            "username": username,
            "password": encrypt_password(
                password
            )
        }
    )


def get_access_token(
    client,
    username,
    password
):

    response = login_user(
        client,
        username,
        password
    )

    assert response.status_code == 200

    return response.json()[
        "access_token"
    ]

# SRS AUTHENTICATION TEST CASES



# AUTH-001: Register Admin
#
# Not applicable.
#
# The application supports only one admin.
# The admin is hardcoded/seeded according
# to the project design and mentor's
# recommendation.
# Public admin registration is intentionally
# not exposed through an API endpoint.




# AUTH-002: Register Student
def test_auth_002_register_student(
    client
):

    response, _, _, _ = create_student(
        client
    )

    assert response.status_code == 200

    data = response.json()

    assert "user_id" in data
    assert "message" in data

    assert data["user_id"] is not None



# AUTH-003: Login Admin
def test_auth_003_login_admin(
    client
):

    response = login_user(
        client,
        "admin",
        "Admin@123"
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data

    assert (
        data["token_type"]
        == "bearer"
    )

    assert (
        data["role"]
        == "admin"
    )


# AUTH-004: Login Student
def test_auth_004_login_student(
    client
):

    (
        register_response,
        username,
        _,
        password
    ) = create_student(
        client
    )

    assert (
        register_response.status_code
        == 200
    )

    response = login_user(
        client,
        username,
        password
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data

    assert (
        data["token_type"]
        == "bearer"
    )

    assert (
        data["role"]
        == "student"
    )


# AUTH-005: Invalid Password
def test_auth_005_invalid_password(
    client
):

    (
        register_response,
        username,
        _,
        _
    ) = create_student(
        client
    )

    assert (
        register_response.status_code
        == 200
    )

    response = login_user(
        client,
        username,
        "WrongPassword@123"
    )

    assert response.status_code == 401


# AUTH-006: Invalid Username
def test_auth_006_invalid_username(
    client
):

    unique = uuid.uuid4().hex[:8]

    response = login_user(
        client,
        f"unknown_user_{unique}",
        "Student@123"
    )

    assert response.status_code == 404


# AUTH-007: Protected API Without Token
def test_auth_007_protected_api_without_token(
    client
):

    response = client.get(
        f"{AUTH_URL}/me"
    )

    assert response.status_code == 401


# AUTH-008: Protected API With Expired Token
def test_auth_008_protected_api_with_expired_token(
    client
):

    expired_payload = {
        "sub": "admin",
        "role": "admin",
        "type": "access",
        "exp": (
            datetime.now(
                timezone.utc
            )
            - timedelta(
                minutes=5
            )
        )
    }

    expired_token = jwt.encode(
        expired_payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    response = client.get(
        f"{AUTH_URL}/me",
        headers={
            "Authorization": (
                f"Bearer {expired_token}"
            )
        }
    )

    assert response.status_code == 401


# ADDITIONAL AUTHENTICATION TEST CASES



# ADDITIONAL: Duplicate Email
def test_duplicate_email(
    client
):

    unique = uuid.uuid4().hex[:8]

    email = f"{unique}@gmail.com"

    first_response, _, _, _ = (
        create_student(
            client,
            username=(
                f"student_one_{unique}"
            ),
            email=email
        )
    )

    assert (
        first_response.status_code
        == 200
    )

    second_response, _, _, _ = (
        create_student(
            client,
            username=(
                f"student_two_{unique}"
            ),
            email=email
        )
    )

    assert (
        second_response.status_code
        == 400
    )



# ADDITIONAL: Duplicate Username
def test_duplicate_username(
    client
):

    unique = uuid.uuid4().hex[:8]

    username = f"student_{unique}"

    first_response, _, _, _ = (
        create_student(
            client,
            username=username,
            email=(
                f"first_{unique}@gmail.com"
            )
        )
    )

    assert (
        first_response.status_code
        == 200
    )

    second_response, _, _, _ = (
        create_student(
            client,
            username=username,
            email=(
                f"second_{unique}@gmail.com"
            )
        )
    )

    assert (
        second_response.status_code
        == 400
    )


# ADDITIONAL: Refresh Token Success
def test_refresh_token_success(
    client
):

    (
        register_response,
        username,
        _,
        password
    ) = create_student(
        client
    )

    assert (
        register_response.status_code
        == 200
    )

    login_response = login_user(
        client,
        username,
        password
    )

    assert (
        login_response.status_code
        == 200
    )

    refresh_token = (
        login_response.json()[
            "refresh_token"
        ]
    )

    response = client.post(
        f"{AUTH_URL}/refresh",
        json={
            "refresh_token": (
                refresh_token
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data

    assert (
        data["token_type"]
        == "bearer"
    )

    assert (
        data["role"]
        == "student"
    )


# ADDITIONAL: Invalid Refresh Token
def test_invalid_refresh_token(
    client
):

    response = client.post(
        f"{AUTH_URL}/refresh",
        json={
            "refresh_token": (
                "invalid.refresh.token"
            )
        }
    )

    assert response.status_code == 401



def test_get_profile(
    client
):

    (
        register_response,
        username,
        email,
        password
    ) = create_student(
        client
    )

    assert (
        register_response.status_code
        == 200
    )

    token = get_access_token(
        client,
        username,
        password
    )

    response = client.get(
        f"{AUTH_URL}/me",
        headers={
            "Authorization": (
                f"Bearer {token}"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["username"]
        == username
    )

    assert (
        data["email"]
        == email
    )

    assert (
        data["role"]
        == "student"
    )

    assert "created_at" in data

# ADDITIONAL: Admin Can Get Users
def test_admin_can_get_users(
    client
):

    token = get_access_token(
        client,
        "admin",
        "Admin@123"
    )

    response = client.get(
        f"{AUTH_URL}/users",
        headers={
            "Authorization": (
                f"Bearer {token}"
            )
        }
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )


# ADDITIONAL: Student Cannot Get Users
def test_student_cannot_get_users(
    client
):

    (
        register_response,
        username,
        _,
        password
    ) = create_student(
        client
    )

    assert (
        register_response.status_code
        == 200
    )

    token = get_access_token(
        client,
        username,
        password
    )

    response = client.get(
        f"{AUTH_URL}/users",
        headers={
            "Authorization": (
                f"Bearer {token}"
            )
        }
    )

    assert response.status_code == 403

# ADDITIONAL: Login Nonexistent User
def test_login_nonexistent_user(
    client
):

    unique = uuid.uuid4().hex[:8]

    response = login_user(
        client,
        f"nonexistent_{unique}",
        "Student@123"
    )

    assert response.status_code == 404

# ADDITIONAL: Invalid Email
def test_register_invalid_email(
    client
):

    unique = uuid.uuid4().hex[:8]

    response = client.post(
        f"{AUTH_URL}/register",
        json={
            "username": (
                f"student_{unique}"
            ),
            "email": "invalid-email",
            "password": encrypt_password(
                "Student@123"
            )
        }
    )

    assert response.status_code == 422


# ADDITIONAL: Empty Username
def test_register_empty_username(
    client
):

    unique = uuid.uuid4().hex[:8]

    response = client.post(
        f"{AUTH_URL}/register",
        json={
            "username": "",
            "email": (
                f"{unique}@gmail.com"
            ),
            "password": encrypt_password(
                "Student@123"
            )
        }
    )

    assert response.status_code == 422


# ADDITIONAL: Password Without Uppercase
def test_register_password_without_uppercase(
    client
):

    unique = uuid.uuid4().hex[:8]

    response = client.post(
        f"{AUTH_URL}/register",
        json={
            "username": (
                f"student_upper_{unique}"
            ),
            "email": (
                f"upper_{unique}@gmail.com"
            ),
            "password": encrypt_password(
                "student@123"
            )
        }
    )

    assert response.status_code == 422


# ADDITIONAL: Password Without Lowercase
def test_register_password_without_lowercase(
    client
):

    unique = uuid.uuid4().hex[:8]

    response = client.post(
        f"{AUTH_URL}/register",
        json={
            "username": (
                f"student_lower_{unique}"
            ),
            "email": (
                f"lower_{unique}@gmail.com"
            ),
            "password": encrypt_password(
                "STUDENT@123"
            )
        }
    )

    assert response.status_code == 422


# ADDITIONAL: Password Without Number
def test_register_password_without_number(
    client
):

    unique = uuid.uuid4().hex[:8]

    response = client.post(
        f"{AUTH_URL}/register",
        json={
            "username": (
                f"student_number_{unique}"
            ),
            "email": (
                f"number_{unique}@gmail.com"
            ),
            "password": encrypt_password(
                "Student@Test"
            )
        }
    )

    assert response.status_code == 422


# ADDITIONAL: Password Without Special Character
def test_register_password_without_special_character(
    client
):

    unique = uuid.uuid4().hex[:8]

    response = client.post(
        f"{AUTH_URL}/register",
        json={
            "username": (
                f"student_special_{unique}"
            ),
            "email": (
                f"special_{unique}@gmail.com"
            ),
            "password": encrypt_password(
                "Student123"
            )
        }
    )

    assert response.status_code == 422


# ADDITIONAL: Password Too Short
def test_register_password_too_short(
    client
):

    unique = uuid.uuid4().hex[:8]

    response = client.post(
        f"{AUTH_URL}/register",
        json={
            "username": (
                f"student_short_{unique}"
            ),
            "email": (
                f"short_{unique}@gmail.com"
            ),
            "password": encrypt_password(
                "Stu@1"
            )
        }
    )

    assert response.status_code == 422


# ADDITIONAL: Password Too Long
def test_register_password_too_long(
    client
):

    unique = uuid.uuid4().hex[:8]

    long_password = (
        "Student@123"
        + ("a" * 30)
    )

    response = client.post(
        f"{AUTH_URL}/register",
        json={
            "username": (
                f"student_long_{unique}"
            ),
            "email": (
                f"long_{unique}@gmail.com"
            ),
            "password": encrypt_password(
                long_password
            )
        }
    )

    assert response.status_code == 422


# ADDITIONAL: Invalid Access Token
def test_invalid_access_token(
    client
):

    response = client.get(
        f"{AUTH_URL}/me",
        headers={
            "Authorization": (
                "Bearer invalid.token.value"
            )
        }
    )

    assert response.status_code == 401


# ========================================
# ADDITIONAL: Missing Access Token
# ========================================


def test_missing_access_token(
    client
):

    response = client.get(
        f"{AUTH_URL}/me"
    )

    assert response.status_code == 401


# ADDITIONAL: Student Cannot Access
# Admin-Only Endpoint
def test_student_cannot_access_admin_endpoint(
    client
):

    (
        register_response,
        username,
        _,
        password
    ) = create_student(
        client
    )

    assert (
        register_response.status_code
        == 200
    )

    token = get_access_token(
        client,
        username,
        password
    )

    response = client.get(
        f"{AUTH_URL}/users",
        headers={
            "Authorization": (
                f"Bearer {token}"
            )
        }
    )

    assert response.status_code == 403