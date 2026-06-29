import pytest

from fastapi.testclient import TestClient

from main import app

from app.core.database import db


@pytest.fixture(scope="session")
def client():

    with TestClient(app) as test_client:

        yield test_client


@pytest.fixture(scope="session")
def admin_token(client):

    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "admin",
            "password": "Admin@123"
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.fixture(scope="session")
def student_token(client):

    client.post(
        "/api/v1/auth/register",
        json={
            "username": "student_test",
            "email": "student_test@gmail.com",
            "password": "Student@123"
        }
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "student_test",
            "password": "Student@123"
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.fixture(scope="session")
def student_headers(student_token):

    return {
        "Authorization": f"Bearer {student_token}"
    }


@pytest.fixture(scope="session")
def admin_headers(admin_token):
    return {
        "Authorization": f"Bearer {admin_token}"
    }


@pytest.fixture(autouse=True)
def clean_categories():

    db["categories"].delete_many({})

    yield

    db["categories"].delete_many({})