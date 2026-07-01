import uuid


AUTH_URL = "/api/v1/auth"


def test_register_student(
    client
):

    unique = uuid.uuid4().hex[:8]

    response = client.post(
        f"{AUTH_URL}/register",
        json={
            "username": f"student_{unique}",
            "email": f"{unique}@gmail.com",
            "password": "Student@123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "user_id" in data

    assert (
        data["message"]
        == "User registered successfully."
    )


def test_duplicate_email(
    client
):

    unique = uuid.uuid4().hex[:8]

    payload = {
        "username": f"student_{unique}",
        "email": f"{unique}@gmail.com",
        "password": "Student@123"
    }

    client.post(
        f"{AUTH_URL}/register",
        json=payload
    )

    response = client.post(
        f"{AUTH_URL}/register",
        json={
            "username": f"another_{unique}",
            "email": payload["email"],
            "password": "Student@123"
        }
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        == "Email already registered."
    )


def test_duplicate_username(
    client
):

    unique = uuid.uuid4().hex[:8]

    payload = {
        "username": f"student_{unique}",
        "email": f"{unique}@gmail.com",
        "password": "Student@123"
    }

    client.post(
        f"{AUTH_URL}/register",
        json=payload
    )

    response = client.post(
        f"{AUTH_URL}/register",
        json={
            "username": payload["username"],
            "email": f"new_{unique}@gmail.com",
            "password": "Student@123"
        }
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        == "Username already exists."
    )


def test_login_success(
    client
):

    unique = uuid.uuid4().hex[:8]

    username = f"student_{unique}"

    password = "Student@123"

    client.post(
        f"{AUTH_URL}/register",
        json={
            "username": username,
            "email": f"{unique}@gmail.com",
            "password": password
        }
    )

    response = client.post(
        f"{AUTH_URL}/login",
        json={
            "username": username,
            "password": password
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data

    assert "refresh_token" in data

    assert data["token_type"] == "bearer"


def test_login_invalid_password(
    client
):

    unique = uuid.uuid4().hex[:8]

    username = f"student_{unique}"

    client.post(
        f"{AUTH_URL}/register",
        json={
            "username": username,
            "email": f"{unique}@gmail.com",
            "password": "Student@123"
        }
    )

    response = client.post(
        f"{AUTH_URL}/login",
        json={
            "username": username,
            "password": "WrongPassword"
        }
    )

    assert response.status_code == 401

    assert (
        response.json()["detail"]
        == "Invalid username or password."
    )

def test_login_user_not_found(
    client
):

    response = client.post(
        f"{AUTH_URL}/login",
        json={
            "username": "unknown_user",
            "password": "Student@123"
        }
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "User not found."
    )

def test_register_invalid_email(
    client
):

    response = client.post(
        f"{AUTH_URL}/register",
        json={
            "username": "student",
            "email": "invalid-email",
            "password": "Student@123"
        }
    )

    assert response.status_code == 422

def test_register_without_username(
    client
):

    response = client.post(
        f"{AUTH_URL}/register",
        json={
            "email": "student@gmail.com",
            "password": "Student@123"
        }
    )

    assert response.status_code == 422

def test_register_without_password(
    client
):

    response = client.post(
        f"{AUTH_URL}/register",
        json={
            "username": "student",
            "email": "student@gmail.com"
        }
    )

    assert response.status_code == 422

def test_refresh_token_success(
    client
):

    unique = uuid.uuid4().hex[:8]

    username = f"student_{unique}"

    password = "Student@123"

    client.post(
        f"{AUTH_URL}/register",
        json={
            "username": username,
            "email": f"{unique}@gmail.com",
            "password": password
        }
    )

    login = client.post(
        f"{AUTH_URL}/login",
        json={
            "username": username,
            "password": password
        }
    )

    refresh_token = login.json()["refresh_token"]

    response = client.post(
        f"{AUTH_URL}/refresh",
        json={
            "refresh_token": refresh_token
        }
    )

    assert response.status_code == 200

    assert "access_token" in response.json()

def test_refresh_token_invalid(
    client
):

    response = client.post(
        f"{AUTH_URL}/refresh",
        json={
            "refresh_token": "invalid_token"
        }
    )

    assert response.status_code == 401

    assert (
        response.json()["detail"]
        == "Invalid or expired token."
    )

def test_get_profile(
    client
):

    unique = uuid.uuid4().hex[:8]

    username = f"student_{unique}"

    password = "Student@123"

    client.post(
        f"{AUTH_URL}/register",
        json={
            "username": username,
            "email": f"{unique}@gmail.com",
            "password": password
        }
    )

    login = client.post(
        f"{AUTH_URL}/login",
        json={
            "username": username,
            "password": password
        }
    )

    token = login.json()["access_token"]

    response = client.get(
        f"{AUTH_URL}/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    assert response.json()["sub"] == username

    assert response.json()["role"] == "student"

    assert response.json()["type"] == "access"


def test_get_profile_without_token(
    client
):

    response = client.get(
        f"{AUTH_URL}/me"
    )

    assert response.status_code == 401

def test_admin_can_get_users(
    client,
    admin_headers
):

    response = client.get(
        f"{AUTH_URL}/users",
        headers=admin_headers
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )

def test_student_cannot_get_users(
    client
):

    unique = uuid.uuid4().hex[:8]

    username = f"student_{unique}"

    password = "Student@123"

    client.post(
        f"{AUTH_URL}/register",
        json={
            "username": username,
            "email": f"{unique}@gmail.com",
            "password": password
        }
    )

    login = client.post(
        f"{AUTH_URL}/login",
        json={
            "username": username,
            "password": password
        }
    )

    token = login.json()["access_token"]

    response = client.get(
        f"{AUTH_URL}/users",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403

    assert (
        response.json()["detail"]
        == "Admin access required."
    )

def test_get_users_without_token(
    client
):

    response = client.get(
        f"{AUTH_URL}/users"
    )

    assert response.status_code == 401

def test_get_users_invalid_token(
    client
):

    response = client.get(
        f"{AUTH_URL}/users",
        headers={
            "Authorization": "Bearer invalidtoken"
        }
    )

    assert response.status_code == 401

def test_register_username_starts_with_number(
    client
):

    response = client.post(
        f"{AUTH_URL}/register",
        json={
            "username": "10student",
            "email": "student1@gmail.com",
            "password": "Student@123"
        }
    )

    assert response.status_code == 422


def test_register_username_with_special_character(
    client
):

    response = client.post(
        f"{AUTH_URL}/register",
        json={
            "username": "student@123",
            "email": "student2@gmail.com",
            "password": "Student@123"
        }
    )

    assert response.status_code == 422


def test_register_username_with_space(
    client
):

    response = client.post(
        f"{AUTH_URL}/register",
        json={
            "username": "student gupta",
            "email": "student3@gmail.com",
            "password": "Student@123"
        }
    )

    assert response.status_code == 422


def test_register_password_without_uppercase(
    client
):

    response = client.post(
        f"{AUTH_URL}/register",
        json={
            "username": "student_upper",
            "email": "student4@gmail.com",
            "password": "student@123"
        }
    )

    assert response.status_code == 422


def test_register_password_without_lowercase(
    client
):

    response = client.post(
        f"{AUTH_URL}/register",
        json={
            "username": "student_lower",
            "email": "student5@gmail.com",
            "password": "STUDENT@123"
        }
    )

    assert response.status_code == 422


def test_register_password_without_number(
    client
):

    response = client.post(
        f"{AUTH_URL}/register",
        json={
            "username": "student_number",
            "email": "student6@gmail.com",
            "password": "Student@"
        }
    )

    assert response.status_code == 422


def test_register_password_without_special_character(
    client
):

    response = client.post(
        f"{AUTH_URL}/register",
        json={
            "username": "student_special",
            "email": "student7@gmail.com",
            "password": "Student123"
        }
    )

    assert response.status_code == 422


def test_register_password_too_short(
    client
):

    response = client.post(
        f"{AUTH_URL}/register",
        json={
            "username": "student_short",
            "email": "student8@gmail.com",
            "password": "Stu@1"
        }
    )

    assert response.status_code == 422