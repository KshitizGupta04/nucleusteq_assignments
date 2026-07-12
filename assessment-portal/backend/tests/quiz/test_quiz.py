import uuid


CATEGORY_URL = "/api/v1/categories"

QUIZ_URL = "/api/v1/quizzes"


def create_category(
    client,
    admin_headers
):

    unique = uuid.uuid4().hex[:8]

    response = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json={
            "name": (
                f"Programming_{unique}"
            ),
            "description": (
                "Programming Category"
            )
        }
    )

    assert response.status_code == 200

    return response.json()[
        "category_id"
    ]


def create_quiz(
    client,
    admin_headers,
    category_id
):

    unique = uuid.uuid4().hex[:8]

    response = client.post(
        QUIZ_URL,
        headers=admin_headers,
        json={
            "title": (
                f"Java Quiz {unique}"
            ),
            "description": (
                "Core Java Quiz"
            ),
            "category_id": category_id,
            "duration": 30,
            "total_marks": 100
        }
    )

    return response


# SRS QUIZ SERVICE TEST CASES


# QUIZ-001: Create Quiz
def test_quiz_001_create_quiz(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    response = create_quiz(
        client,
        admin_headers,
        category_id
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        == "Quiz created successfully."
    )

    assert "quiz_id" in response.json()


# QUIZ-002: Create Duplicate Quiz
def test_quiz_002_create_duplicate_quiz(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    unique = uuid.uuid4().hex[:8]

    payload = {
        "title": (
            f"Java Quiz {unique}"
        ),
        "description": "Core Java Quiz",
        "category_id": category_id,
        "duration": 30,
        "total_marks": 100
    }

    first_response = client.post(
        QUIZ_URL,
        headers=admin_headers,
        json=payload
    )

    assert first_response.status_code == 200

    response = client.post(
        QUIZ_URL,
        headers=admin_headers,
        json=payload
    )

    assert response.status_code == 400


# QUIZ-003: Get All Quizzes
def test_quiz_003_get_all_quizzes(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    create_response = create_quiz(
        client,
        admin_headers,
        category_id
    )

    assert create_response.status_code == 200

    response = client.get(
        QUIZ_URL,
        headers=admin_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data,
        list
    )

    assert len(data) == 1


# QUIZ-004: Update Quiz
def test_quiz_004_update_quiz(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    quiz = create_quiz(
        client,
        admin_headers,
        category_id
    )

    assert quiz.status_code == 200

    quiz_id = quiz.json()[
        "quiz_id"
    ]

    response = client.put(
        f"{QUIZ_URL}/{quiz_id}",
        headers=admin_headers,
        json={
            "title": "Advanced Java",
            "description": (
                "Updated Java Quiz"
            ),
            "category_id": category_id,
            "duration": 45,
            "total_marks": 150
        }
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        == "Quiz updated successfully."
    )


# QUIZ-005: Update Non-Existing Quiz
def test_quiz_005_update_non_existing_quiz(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    response = client.put(
        (
            f"{QUIZ_URL}/"
            "684fd8d32ab5a11111111111"
        ),
        headers=admin_headers,
        json={
            "title": "Java Quiz",
            "description": "Java Quiz",
            "category_id": category_id,
            "duration": 30,
            "total_marks": 100
        }
    )

    assert response.status_code == 404


# QUIZ-006: Delete Quiz
def test_quiz_006_delete_quiz(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    quiz = create_quiz(
        client,
        admin_headers,
        category_id
    )

    assert quiz.status_code == 200

    quiz_id = quiz.json()[
        "quiz_id"
    ]

    response = client.delete(
        f"{QUIZ_URL}/{quiz_id}",
        headers=admin_headers
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        == "Quiz deleted successfully."
    )


# QUIZ-007: Delete Invalid Quiz
def test_quiz_007_delete_invalid_quiz(
    client,
    admin_headers
):

    response = client.delete(
        (
            f"{QUIZ_URL}/"
            "684fd8d32ab5a11111111111"
        ),
        headers=admin_headers
    )

    assert response.status_code == 404


# ADDITIONAL QUIZ TEST CASES
# ADDITIONAL: Invalid Category
def test_invalid_category(
    client,
    admin_headers
):

    response = client.post(
        QUIZ_URL,
        headers=admin_headers,
        json={
            "title": "Python Quiz",
            "description": "Python Quiz",
            "category_id": (
                "684fd8d32ab5a11111111111"
            ),
            "duration": 30,
            "total_marks": 100
        }
    )

    assert response.status_code == 404


# ADDITIONAL: Create Without Title
def test_create_quiz_without_title(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    response = client.post(
        QUIZ_URL,
        headers=admin_headers,
        json={
            "description": "Java Quiz",
            "category_id": category_id,
            "duration": 30,
            "total_marks": 100
        }
    )

    assert response.status_code == 422


# ADDITIONAL: Create Without Description
def test_create_quiz_without_description(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    response = client.post(
        QUIZ_URL,
        headers=admin_headers,
        json={
            "title": "Java Quiz",
            "category_id": category_id,
            "duration": 30,
            "total_marks": 100
        }
    )

    assert response.status_code == 422


# ADDITIONAL: Create Without Category
def test_create_quiz_without_category(
    client,
    admin_headers
):

    response = client.post(
        QUIZ_URL,
        headers=admin_headers,
        json={
            "title": "Java Quiz",
            "description": "Java Quiz",
            "duration": 30,
            "total_marks": 100
        }
    )

    assert response.status_code == 422


# ADDITIONAL: Invalid Duration
def test_create_quiz_invalid_duration(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    response = client.post(
        QUIZ_URL,
        headers=admin_headers,
        json={
            "title": "Java Quiz",
            "description": "Java Quiz",
            "category_id": category_id,
            "duration": 0,
            "total_marks": 100
        }
    )

    assert response.status_code == 422


# ADDITIONAL: Invalid Total Marks
def test_create_quiz_invalid_total_marks(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    response = client.post(
        QUIZ_URL,
        headers=admin_headers,
        json={
            "title": "Java Quiz",
            "description": "Java Quiz",
            "category_id": category_id,
            "duration": 30,
            "total_marks": 0
        }
    )

    assert response.status_code == 422


# ADDITIONAL: Short Title
def test_create_quiz_short_title(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    response = client.post(
        QUIZ_URL,
        headers=admin_headers,
        json={
            "title": "Ja",
            "description": "Java Quiz",
            "category_id": category_id,
            "duration": 30,
            "total_marks": 100
        }
    )

    assert response.status_code == 422


# ADDITIONAL: Short Description
def test_create_quiz_short_description(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    response = client.post(
        QUIZ_URL,
        headers=admin_headers,
        json={
            "title": "Java Quiz",
            "description": "abc",
            "category_id": category_id,
            "duration": 30,
            "total_marks": 100
        }
    )

    assert response.status_code == 422


# ADDITIONAL: Create Without Token
def test_create_quiz_without_token(
    client
):

    response = client.post(
        QUIZ_URL,
        json={
            "title": "Java Quiz",
            "description": "Java Quiz",
            "category_id": (
                "123456789012345678901234"
            ),
            "duration": 30,
            "total_marks": 100
        }
    )

    assert response.status_code == 401


# ADDITIONAL: Update Without Token
def test_update_quiz_without_token(
    client
):

    response = client.put(
        (
            f"{QUIZ_URL}/"
            "123456789012345678901234"
        ),
        json={
            "title": "Java Quiz",
            "description": "Java Quiz",
            "category_id": (
                "123456789012345678901234"
            ),
            "duration": 30,
            "total_marks": 100
        }
    )

    assert response.status_code == 401


# ADDITIONAL: Delete Without Token
def test_delete_quiz_without_token(
    client
):

    response = client.delete(
        (
            f"{QUIZ_URL}/"
            "123456789012345678901234"
        )
    )

    assert response.status_code == 401


# ADDITIONAL: Student Cannot Create Quiz
def test_student_cannot_create_quiz(
    client,
    student_headers
):

    response = client.post(
        QUIZ_URL,
        headers=student_headers,
        json={
            "title": "Java Quiz",
            "description": "Java Quiz",
            "category_id": (
                "123456789012345678901234"
            ),
            "duration": 30,
            "total_marks": 100
        }
    )

    assert response.status_code == 403


# ADDITIONAL: Student Cannot Update Quiz
def test_student_cannot_update_quiz(
    client,
    student_headers
):

    response = client.put(
        (
            f"{QUIZ_URL}/"
            "123456789012345678901234"
        ),
        headers=student_headers,
        json={
            "title": "Java Quiz",
            "description": "Java Quiz",
            "category_id": (
                "123456789012345678901234"
            ),
            "duration": 30,
            "total_marks": 100
        }
    )

    assert response.status_code == 403


# ADDITIONAL: Student Cannot Delete Quiz
def test_student_cannot_delete_quiz(
    client,
    student_headers
):

    response = client.delete(
        (
            f"{QUIZ_URL}/"
            "123456789012345678901234"
        ),
        headers=student_headers
    )

    assert response.status_code == 403