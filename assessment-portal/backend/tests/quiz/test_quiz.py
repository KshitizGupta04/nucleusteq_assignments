import uuid


AUTH_URL = "/api/v1/auth"

CATEGORY_URL = "/api/v1/categories"

QUIZ_URL = "/api/v1/quizzes"


def get_admin_token(
    client
):

    response = client.post(
        f"{AUTH_URL}/login",
        json={
            "username": "admin",
            "password": "Admin@123"
        }
    )

    return response.json()["access_token"]


def create_category(
    client,
    token
):

    unique = uuid.uuid4().hex[:8]

    response = client.post(
        CATEGORY_URL,
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": f"Programming_{unique}",
            "description": "Programming Category"
        }
    )

    return response.json()["category_id"]


def create_quiz(
    client,
    token,
    category_id
):

    unique = uuid.uuid4().hex[:8]

    response = client.post(
        QUIZ_URL,
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": f"Java Quiz {unique}",
            "description": "Core Java Quiz",
            "category_id": category_id,
            "duration": 30,
            "total_marks": 100
        }
    )

    return response


def test_create_quiz(
    client
):

    token = get_admin_token(
        client
    )

    category_id = create_category(
        client,
        token
    )

    response = create_quiz(
        client,
        token,
        category_id
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        == "Quiz created successfully."
    )


def test_get_all_quizzes(
    client
):

    token = get_admin_token(
        client
    )

    response = client.get(
        QUIZ_URL,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )


def test_update_quiz(
    client
):

    token = get_admin_token(
        client
    )

    category_id = create_category(
        client,
        token
    )

    quiz = create_quiz(
        client,
        token,
        category_id
    )

    quiz_id = quiz.json()["quiz_id"]

    response = client.put(
        f"{QUIZ_URL}/{quiz_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Advanced Java",
            "description": "Updated Quiz",
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


def test_delete_quiz(
    client
):

    token = get_admin_token(
        client
    )

    category_id = create_category(
        client,
        token
    )

    quiz = create_quiz(
        client,
        token,
        category_id
    )

    quiz_id = quiz.json()["quiz_id"]

    response = client.delete(
        f"{QUIZ_URL}/{quiz_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        == "Quiz deleted successfully."
    )


def test_duplicate_quiz(
    client
):

    token = get_admin_token(
        client
    )

    category_id = create_category(
        client,
        token
    )

    unique = uuid.uuid4().hex[:8]

    payload = {
        "title": f"Java Quiz {unique}",
        "description": "Core Java Quiz",
        "category_id": category_id,
        "duration": 30,
        "total_marks": 100
    }

    client.post(
        QUIZ_URL,
        headers={
            "Authorization": f"Bearer {token}"
        },
        json=payload
    )

    response = client.post(
        QUIZ_URL,
        headers={
            "Authorization": f"Bearer {token}"
        },
        json=payload
    )

    assert response.status_code == 400


def test_invalid_category(
    client
):

    token = get_admin_token(
        client
    )

    response = client.post(
        QUIZ_URL,
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Python",
            "description": "Python Quiz",
            "category_id": "684fd8d32ab5a11111111111",
            "duration": 30,
            "total_marks": 100
        }
    )

    assert response.status_code == 404


def test_update_invalid_quiz(
    client
):

    token = get_admin_token(
        client
    )

    category_id = create_category(
        client,
        token
    )

    response = client.put(
        f"{QUIZ_URL}/684fd8d32ab5a11111111111",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Java",
            "description": "Java Quiz",
            "category_id": category_id,
            "duration": 30,
            "total_marks": 100
        }
    )

    assert response.status_code == 404


def test_delete_invalid_quiz(
    client
):

    token = get_admin_token(
        client
    )

    response = client.delete(
        f"{QUIZ_URL}/684fd8d32ab5a11111111111",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404

def test_create_quiz_without_title(
    client
):

    token = get_admin_token(client)

    category_id = create_category(
        client,
        token
    )

    response = client.post(
        QUIZ_URL,
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "description": "Java Quiz",
            "category_id": category_id,
            "duration": 30,
            "total_marks": 100
        }
    )

    assert response.status_code == 422

def test_create_quiz_without_description(
    client
):

    token = get_admin_token(client)

    category_id = create_category(
        client,
        token
    )

    response = client.post(
        QUIZ_URL,
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Java",
            "category_id": category_id,
            "duration": 30,
            "total_marks": 100
        }
    )

    assert response.status_code == 422

def test_create_quiz_without_category(
    client
):

    token = get_admin_token(client)

    response = client.post(
        QUIZ_URL,
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Java",
            "description": "Java Quiz",
            "duration": 30,
            "total_marks": 100
        }
    )

    assert response.status_code == 422

def test_create_quiz_invalid_duration(
    client
):

    token = get_admin_token(client)

    category_id = create_category(
        client,
        token
    )

    response = client.post(
        QUIZ_URL,
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Java",
            "description": "Java Quiz",
            "category_id": category_id,
            "duration": 0,
            "total_marks": 100
        }
    )

    assert response.status_code == 422

def test_create_quiz_invalid_total_marks(
    client
):

    token = get_admin_token(client)

    category_id = create_category(
        client,
        token
    )

    response = client.post(
        QUIZ_URL,
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Java",
            "description": "Java Quiz",
            "category_id": category_id,
            "duration": 30,
            "total_marks": 0
        }
    )

    assert response.status_code == 422

def test_create_quiz_short_title(
    client
):

    token = get_admin_token(client)

    category_id = create_category(
        client,
        token
    )

    response = client.post(
        QUIZ_URL,
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Ja",
            "description": "Java Quiz",
            "category_id": category_id,
            "duration": 30,
            "total_marks": 100
        }
    )

    assert response.status_code == 422

def test_create_quiz_short_description(
    client
):

    token = get_admin_token(client)

    category_id = create_category(
        client,
        token
    )

    response = client.post(
        QUIZ_URL,
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Java",
            "description": "abc",
            "category_id": category_id,
            "duration": 30,
            "total_marks": 100
        }
    )

    assert response.status_code == 422

def test_create_quiz_without_token(
    client
):

    response = client.post(
        QUIZ_URL,
        json={
            "title": "Java",
            "description": "Java Quiz",
            "category_id": "123",
            "duration": 30,
            "total_marks": 100
        }
    )

    assert response.status_code == 401

def test_update_quiz_without_token(
    client
):

    response = client.put(
        f"{QUIZ_URL}/123456789012345678901234",
        json={
            "title": "Java",
            "description": "Java Quiz",
            "category_id": "123456789012345678901234",
            "duration": 30,
            "total_marks": 100
        }
    )

    assert response.status_code == 401

def test_delete_quiz_without_token(
    client
):

    response = client.delete(
        f"{QUIZ_URL}/123456789012345678901234"
    )

    assert response.status_code == 401

def test_student_cannot_create_quiz(
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

    response = client.post(
        QUIZ_URL,
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Java",
            "description": "Java Quiz",
            "category_id": "123456789012345678901234",
            "duration": 30,
            "total_marks": 100
        }
    )

    assert response.status_code == 403

def test_student_cannot_update_quiz(
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

    response = client.put(
        f"{QUIZ_URL}/123456789012345678901234",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Java",
            "description": "Java Quiz",
            "category_id": "123456789012345678901234",
            "duration": 30,
            "total_marks": 100
        }
    )

    assert response.status_code == 403

def test_student_cannot_delete_quiz(
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

    response = client.delete(
        f"{QUIZ_URL}/123456789012345678901234",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403
    