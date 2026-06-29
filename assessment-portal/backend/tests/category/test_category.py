import pytest

from app.core.database import db


CATEGORY_URL = "/api/v1/categories/"


def test_create_category(
    client,
    admin_headers
):

    response = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json={
            "name": "Java",
            "description": "Java Programming"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "category_id" in data

    assert (
        data["message"]
        == "Category created successfully."
    )


def test_get_categories(
    client,
    admin_headers
):

    client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json={
            "name": "Python",
            "description": "Python Programming"
        }
    )

    response = client.get(
        CATEGORY_URL,
        headers=admin_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    assert data[0]["name"] == "Python"

    assert (
        data[0]["description"]
        == "Python Programming"
    )


def test_update_category(
    client,
    admin_headers
):

    create_response = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json={
            "name": "React",
            "description": "Frontend Library"
        }
    )

    category_id = (
        create_response.json()["category_id"]
    )

    response = client.put(
        f"{CATEGORY_URL}{category_id}",
        headers=admin_headers,
        json={
            "name": "React JS",
            "description": "Frontend JavaScript Library"
        }
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        == "Category updated successfully."
    )


def test_delete_category(
    client,
    admin_headers
):

    create_response = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json={
            "name": "Node",
            "description": "Backend Runtime"
        }
    )

    category_id = (
        create_response.json()["category_id"]
    )

    response = client.delete(
        f"{CATEGORY_URL}{category_id}",
        headers=admin_headers
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        == "Category deleted successfully."
    )

    assert (
        db["categories"].count_documents({})
        == 0
    )


def test_create_duplicate_category(
    client,
    admin_headers
):

    payload = {
        "name": "Java",
        "description": "Java Programming"
    }

    client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json=payload
    )

    response = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json=payload
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        == "Category already exists."
    )


def test_create_category_with_empty_name(
    client,
    admin_headers
):

    response = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json={
            "name": "",
            "description": "Programming"
        }
    )

    assert response.status_code == 422


def test_create_category_with_empty_description(
    client,
    admin_headers
):

    response = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json={
            "name": "Python",
            "description": ""
        }
    )

    assert response.status_code == 422


def test_get_empty_categories(
    client,
    admin_headers
):

    response = client.get(
        CATEGORY_URL,
        headers=admin_headers
    )

    assert response.status_code == 200

    assert response.json() == []


def test_update_non_existing_category(
    client,
    admin_headers
):

    response = client.put(
        f"{CATEGORY_URL}685f8f5d6d8b7d6c12345678",
        headers=admin_headers,
        json={
            "name": "Updated",
            "description": "Updated Description"
        }
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Category not found."
    )

def test_delete_non_existing_category(
    client,
    admin_headers
):

    response = client.delete(
        f"{CATEGORY_URL}685f8f5d6d8b7d6c12345678",
        headers=admin_headers
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Category not found."
    )

def test_create_category_without_name(
    client,
    admin_headers
):

    response = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json={
            "description": "Programming"
        }
    )

    assert response.status_code == 422

def test_create_category_without_description(
    client,
    admin_headers
):

    response = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json={
            "name": "Java"
        }
    )

    assert response.status_code == 422

def test_create_category_name_too_short(
    client,
    admin_headers
):

    response = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json={
            "name": "Ja",
            "description": "Programming"
        }
    )

    assert response.status_code == 422

def test_create_category_description_too_short(
    client,
    admin_headers
):

    response = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json={
            "name": "Java",
            "description": "abc"
        }
    )

    assert response.status_code == 422

def test_student_cannot_create_category(
    client,
    student_headers
):

    response = client.post(
        CATEGORY_URL,
        headers=student_headers,
        json={
            "name": "Java",
            "description": "Java Programming"
        }
    )

    assert response.status_code == 403

def test_student_cannot_update_category(
    client,
    admin_headers,
    student_headers
):

    create = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json={
            "name": "React",
            "description": "Frontend Library"
        }
    )

    category_id = create.json()["category_id"]

    response = client.put(
        f"{CATEGORY_URL}{category_id}",
        headers=student_headers,
        json={
            "name": "React JS",
            "description": "Frontend JavaScript Library"
        }
    )

    assert response.status_code == 403

def test_student_cannot_delete_category(
    client,
    admin_headers,
    student_headers
):

    create = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json={
            "name": "Node",
            "description": "Backend Runtime"
        }
    )

    category_id = create.json()["category_id"]

    response = client.delete(
        f"{CATEGORY_URL}{category_id}",
        headers=student_headers
    )

    assert response.status_code == 403

def test_student_can_get_categories(
    client,
    student_headers
):

    response = client.get(
        CATEGORY_URL,
        headers=student_headers
    )

    assert response.status_code == 200

def test_update_category_with_duplicate_name(
    client,
    admin_headers
):

    first = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json={
            "name": "Java",
            "description": "Java Programming"
        }
    )

    second = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json={
            "name": "Python",
            "description": "Python Programming"
        }
    )

    category_id = second.json()["category_id"]

    response = client.put(
        f"{CATEGORY_URL}{category_id}",
        headers=admin_headers,
        json={
            "name": "Java",
            "description": "Updated Description"
        }
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        == "Category already exists."
    )

def test_update_invalid_object_id(
    client,
    admin_headers
):

    response = client.put(
        f"{CATEGORY_URL}abc",
        headers=admin_headers,
        json={
            "name": "Java",
            "description": "Programming"
        }
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Category not found."
    )

def test_delete_invalid_object_id(
    client,
    admin_headers
):

    response = client.delete(
        f"{CATEGORY_URL}abc",
        headers=admin_headers
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Category not found."
    )

def test_category_name_too_long(
    client,
    admin_headers
):

    response = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json={
            "name": "A" * 101,
            "description": "Programming"
        }
    )

    assert response.status_code == 422

def test_category_description_too_long(
    client,
    admin_headers
):

    response = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json={
            "name": "Java",
            "description": "A" * 256
        }
    )

    assert response.status_code == 422