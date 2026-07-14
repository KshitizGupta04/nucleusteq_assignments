from app.core.database import db


CATEGORY_URL = "/api/v1/categories/"


# SRS CATEGORY SERVICE TEST CASES


# CAT-001: Create Category
def test_cat_001_create_category(
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


# CAT-002: Create Duplicate Category
def test_cat_002_create_duplicate_category(
    client,
    admin_headers
):

    payload = {
        "name": "Java",
        "description": "Java Programming"
    }

    first_response = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json=payload
    )

    assert first_response.status_code == 200

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


# CAT-003: Get Categories
def test_cat_003_get_categories(
    client,
    admin_headers
):

    create_response = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json={
            "name": "Python",
            "description": "Python Programming"
        }
    )

    assert create_response.status_code == 200

    response = client.get(
        CATEGORY_URL,
        headers=admin_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data,
        list
    )

    assert len(data) == 1

    assert (
        data[0]["name"]
        == "Python"
    )

    assert (
        data[0]["description"]
        == "Python Programming"
    )

# CAT-004: Update Category
def test_cat_004_update_category(
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

    assert create_response.status_code == 200

    category_id = (
        create_response.json()[
            "category_id"
        ]
    )

    response = client.put(
        f"{CATEGORY_URL}{category_id}",
        headers=admin_headers,
        json={
            "name": "React JS",
            "description": (
                "Frontend JavaScript Library"
            )
        }
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        == "Category updated successfully."
    )



# CAT-005: Update Non-Existing Category
def test_cat_005_update_non_existing_category(
    client,
    admin_headers
):

    response = client.put(
        (
            f"{CATEGORY_URL}"
            "685f8f5d6d8b7d6c12345678"
        ),
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



# CAT-006: Delete Category
def test_cat_006_delete_category(
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

    assert create_response.status_code == 200

    category_id = (
        create_response.json()[
            "category_id"
        ]
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



# CAT-007: Delete Invalid Category
def test_cat_007_delete_invalid_category(
    client,
    admin_headers
):

    response = client.delete(
        (
            f"{CATEGORY_URL}"
            "685f8f5d6d8b7d6c12345678"
        ),
        headers=admin_headers
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Category not found."
    )



# ADDITIONAL CATEGORY TEST CASES



# ADDITIONAL: Empty Category Name
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



# ADDITIONAL: Empty Description
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



# ADDITIONAL: Get Empty Categories
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



# ADDITIONAL: Missing Category Name
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



# ADDITIONAL: Missing Description
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



# ADDITIONAL: Category Name Too Short
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



# ADDITIONAL: Description Too Short
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



# ADDITIONAL: Student Cannot Create
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



# ADDITIONAL: Student Cannot Update
def test_student_cannot_update_category(
    client,
    admin_headers,
    student_headers
):

    create_response = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json={
            "name": "React",
            "description": "Frontend Library"
        }
    )

    assert create_response.status_code == 200

    category_id = (
        create_response.json()[
            "category_id"
        ]
    )

    response = client.put(
        f"{CATEGORY_URL}{category_id}",
        headers=student_headers,
        json={
            "name": "React JS",
            "description": (
                "Frontend JavaScript Library"
            )
        }
    )

    assert response.status_code == 403



# ADDITIONAL: Student Cannot Delete
def test_student_cannot_delete_category(
    client,
    admin_headers,
    student_headers
):

    create_response = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json={
            "name": "Node",
            "description": "Backend Runtime"
        }
    )

    assert create_response.status_code == 200

    category_id = (
        create_response.json()[
            "category_id"
        ]
    )

    response = client.delete(
        f"{CATEGORY_URL}{category_id}",
        headers=student_headers
    )

    assert response.status_code == 403



# ADDITIONAL: Student Can Get Categories
def test_student_can_get_categories(
    client,
    student_headers
):

    response = client.get(
        CATEGORY_URL,
        headers=student_headers
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )



# ADDITIONAL: Update With Duplicate Name
def test_update_category_with_duplicate_name(
    client,
    admin_headers
):

    first_response = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json={
            "name": "Java",
            "description": "Java Programming"
        }
    )

    assert first_response.status_code == 200

    second_response = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json={
            "name": "Python",
            "description": "Python Programming"
        }
    )

    assert second_response.status_code == 200

    category_id = (
        second_response.json()[
            "category_id"
        ]
    )

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



# ADDITIONAL: Update Invalid Object ID
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



# ADDITIONAL: Delete Invalid Object ID
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



# ADDITIONAL: Category Name Too Long
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


# ADDITIONAL: Description Too Long
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



# ADDITIONAL: Get Category By ID
def test_get_category_by_id(
    client,
    admin_headers
):

    create_response = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json={
            "name": "Java",
            "description": "Java Category"
        }
    )

    assert create_response.status_code == 200

    category_id = (
        create_response.json()[
            "category_id"
        ]
    )

    response = client.get(
        f"{CATEGORY_URL}{category_id}",
        headers=admin_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["id"]
        == category_id
    )

    assert (
        data["name"]
        == "Java"
    )

    assert (
        data["description"]
        == "Java Category"
    )



# ADDITIONAL: Get Non-Existing Category
def test_get_category_invalid_id(
    client,
    admin_headers
):

    response = client.get(
        (
            f"{CATEGORY_URL}"
            "689999999999999999999999"
        ),
        headers=admin_headers
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Category not found."
    )



# ADDITIONAL: Get Category Without Token
def test_get_category_without_token(
    client
):

    response = client.get(
        (
            f"{CATEGORY_URL}"
            "689999999999999999999999"
        )
    )

    assert response.status_code == 401



# ADDITIONAL: Get Category Invalid Token
def test_get_category_invalid_token(
    client
):

    response = client.get(
        (
            f"{CATEGORY_URL}"
            "689999999999999999999999"
        ),
        headers={
            "Authorization": (
                "Bearer invalidtoken"
            )
        }
    )

    assert response.status_code == 401