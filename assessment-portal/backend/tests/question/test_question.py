import uuid

CATEGORY_URL = "/api/v1/categories"
QUIZ_URL = "/api/v1/quizzes"
QUESTION_URL = "/api/v1/questions"


def create_category(
    client,
    admin_headers
):

    unique = uuid.uuid4().hex[:8]

    response = client.post(
        CATEGORY_URL + "/",
        json={
            "name": f"Category_{unique}",
            "description": "Programming Category"
        },
        headers=admin_headers
    )

    assert response.status_code == 200

    return response.json()["category_id"]


def create_quiz(
    client,
    admin_headers,
    category_id
):

    unique = uuid.uuid4().hex[:8]

    response = client.post(
        QUIZ_URL + "/",
        json={
            "title": f"Quiz_{unique}",
            "description": "Quiz Description",
            "category_id": category_id,
            "duration": 30,
            "total_marks": 100
        },
        headers=admin_headers
    )

    assert response.status_code == 200

    return response.json()["quiz_id"]


def create_question(
    client,
    admin_headers,
    quiz_id
):

    response = client.post(
        QUESTION_URL + "/",
        json={
            "quiz_id": quiz_id,
            "question": "What is Java Programming?",
            "options": [
                "Programming Language",
                "Database",
                "Browser",
                "Operating System"
            ],
            "correct_answer": "Programming Language",
            "question_type": "mcq",
            "difficulty": "easy"
        },
        headers=admin_headers
    )

    assert response.status_code == 200

    return response.json()["question_id"]


# QST-001 Add MCQ Question

def test_qst_001_add_mcq_question(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    quiz_id = create_quiz(
        client,
        admin_headers,
        category_id
    )

    response = client.post(
        QUESTION_URL + "/",
        json={
            "quiz_id": quiz_id,
            "question": "Which language is platform independent?",
            "options": [
                "Java",
                "C",
                "Python",
                "HTML"
            ],
            "correct_answer": "Java",
            "question_type": "mcq",
            "difficulty": "easy"
        },
        headers=admin_headers
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        == "Question created successfully."
    )


# QST-002 Add True False Question

def test_qst_002_add_true_false_question(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    quiz_id = create_quiz(
        client,
        admin_headers,
        category_id
    )

    response = client.post(
        QUESTION_URL + "/",
        json={
            "quiz_id": quiz_id,
            "question": "Java is object oriented.",
            "options": [
                "True",
                "False",
                "NA",
                "None"
            ],
            "correct_answer": "True",
            "question_type": "true_false",
            "difficulty": "easy"
        },
        headers=admin_headers
    )

    assert response.status_code == 200



# QST-003 Missing Answer
def test_qst_003_missing_answer(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    quiz_id = create_quiz(
        client,
        admin_headers,
        category_id
    )

    response = client.post(
        QUESTION_URL + "/",
        json={
            "quiz_id": quiz_id,
            "question": "Missing answer question",
            "options": [
                "A",
                "B",
                "C",
                "D"
            ],
            "question_type": "mcq",
            "difficulty": "easy"
        },
        headers=admin_headers
    )

    assert response.status_code == 422



# QST-004 Update Question
def test_qst_004_update_question(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    quiz_id = create_quiz(
        client,
        admin_headers,
        category_id
    )

    question_id = create_question(
        client,
        admin_headers,
        quiz_id
    )

    response = client.put(
        f"{QUESTION_URL}/{question_id}",
        json={
            "question": "Updated Java Question",
            "options": [
                "Java",
                "Python",
                "HTML",
                "CSS"
            ],
            "correct_answer": "Java",
            "question_type": "mcq",
            "difficulty": "medium"
        },
        headers=admin_headers
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        == "Question updated successfully."
    )


# QST-005 Delete Question
def test_qst_005_delete_question(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    quiz_id = create_quiz(
        client,
        admin_headers,
        category_id
    )

    question_id = create_question(
        client,
        admin_headers,
        quiz_id
    )

    response = client.delete(
        f"{QUESTION_URL}/{question_id}",
        headers=admin_headers
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        == "Question deleted successfully."
    )



# QST-006 Get Questions By Quiz

def test_qst_006_get_questions_by_quiz(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    quiz_id = create_quiz(
        client,
        admin_headers,
        category_id
    )

    create_question(
        client,
        admin_headers,
        quiz_id
    )

    response = client.get(
        f"{QUESTION_URL}/quiz/{quiz_id}",
        headers=admin_headers
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )

    assert len(
        response.json()
    ) >= 1



# QST-007 Invalid Quiz Id
def test_qst_007_invalid_quiz_id(
    client,
    admin_headers
):

    response = client.post(
        QUESTION_URL + "/",
        json={
            "quiz_id": "689999999999999999999999",
            "question": "Invalid Quiz Question",
            "options": [
                "A",
                "B",
                "C",
                "D"
            ],
            "correct_answer": "A",
            "question_type": "mcq",
            "difficulty": "easy"
        },
        headers=admin_headers
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Quiz not found."
    )



# Invalid Question Id
def test_update_invalid_question(
    client,
    admin_headers
):

    response = client.put(
        f"{QUESTION_URL}/689999999999999999999999",
        json={
            "question": "Updated Question",
            "options": [
                "A",
                "B",
                "C",
                "D"
            ],
            "correct_answer": "A",
            "question_type": "mcq",
            "difficulty": "easy"
        },
        headers=admin_headers
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Question not found."
    )


def test_delete_invalid_question(
    client,
    admin_headers
):

    response = client.delete(
        f"{QUESTION_URL}/689999999999999999999999",
        headers=admin_headers
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Question not found."
    )



# Student Cannot Create Question
def test_student_cannot_create_question(
    client
):

    unique = uuid.uuid4().hex[:8]

    client.post(
        "/api/v1/auth/register",
        json={
            "username": f"student_{unique}",
            "email": f"{unique}@gmail.com",
            "password": "Student@123"
        }
    )

    login = client.post(
        "/api/v1/auth/login",
        json={
            "username": f"student_{unique}",
            "password": "Student@123"
        }
    )

    token = login.json()["access_token"]

    response = client.post(
        QUESTION_URL + "/",
        json={
            "quiz_id": "689999999999999999999999",
            "question": "Student Question",
            "options": [
                "A",
                "B",
                "C",
                "D"
            ],
            "correct_answer": "A",
            "question_type": "mcq",
            "difficulty": "easy"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403



# Student Cannot Update Question

def test_student_cannot_update_question(
    client
):

    unique = uuid.uuid4().hex[:8]

    client.post(
        "/api/v1/auth/register",
        json={
            "username": f"student_{unique}",
            "email": f"{unique}@gmail.com",
            "password": "Student@123"
        }
    )

    login = client.post(
        "/api/v1/auth/login",
        json={
            "username": f"student_{unique}",
            "password": "Student@123"
        }
    )

    token = login.json()["access_token"]

    response = client.put(
        f"{QUESTION_URL}/689999999999999999999999",
        json={
            "question": "Updated",
            "options": [
                "A",
                "B",
                "C",
                "D"
            ],
            "correct_answer": "A",
            "question_type": "mcq",
            "difficulty": "easy"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403


# Student Cannot Delete Question

def test_student_cannot_delete_question(
    client
):

    unique = uuid.uuid4().hex[:8]

    client.post(
        "/api/v1/auth/register",
        json={
            "username": f"student_{unique}",
            "email": f"{unique}@gmail.com",
            "password": "Student@123"
        }
    )

    login = client.post(
        "/api/v1/auth/login",
        json={
            "username": f"student_{unique}",
            "password": "Student@123"
        }
    )

    token = login.json()["access_token"]

    response = client.delete(
        f"{QUESTION_URL}/689999999999999999999999",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403


# Validation Tests
def test_question_too_short(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    quiz_id = create_quiz(
        client,
        admin_headers,
        category_id
    )

    response = client.post(
        QUESTION_URL + "/",
        json={
            "quiz_id": quiz_id,
            "question": "Test",
            "options": [
                "A",
                "B",
                "C",
                "D"
            ],
            "correct_answer": "A",
            "question_type": "mcq",
            "difficulty": "easy"
        },
        headers=admin_headers
    )

    assert response.status_code == 422


def test_less_than_four_options(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    quiz_id = create_quiz(
        client,
        admin_headers,
        category_id
    )

    response = client.post(
        QUESTION_URL + "/",
        json={
            "quiz_id": quiz_id,
            "question": "Sample Question",
            "options": [
                "A",
                "B"
            ],
            "correct_answer": "A",
            "question_type": "mcq",
            "difficulty": "easy"
        },
        headers=admin_headers
    )

    assert response.status_code == 422


def test_correct_answer_not_in_options(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    quiz_id = create_quiz(
        client,
        admin_headers,
        category_id
    )

    response = client.post(
        QUESTION_URL + "/",
        json={
            "quiz_id": quiz_id,
            "question": "Sample Question",
            "options": [
                "A",
                "B",
                "C",
                "D"
            ],
            "correct_answer": "E",
            "question_type": "mcq",
            "difficulty": "easy"
        },
        headers=admin_headers
    )

    assert response.status_code == 422


def test_invalid_question_type(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    quiz_id = create_quiz(
        client,
        admin_headers,
        category_id
    )

    response = client.post(
        QUESTION_URL + "/",
        json={
            "quiz_id": quiz_id,
            "question": "Sample Question",
            "options": [
                "A",
                "B",
                "C",
                "D"
            ],
            "correct_answer": "A",
            "question_type": "coding",
            "difficulty": "easy"
        },
        headers=admin_headers
    )

    assert response.status_code == 422


def test_invalid_difficulty(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    quiz_id = create_quiz(
        client,
        admin_headers,
        category_id
    )

    response = client.post(
        QUESTION_URL + "/",
        json={
            "quiz_id": quiz_id,
            "question": "Sample Question",
            "options": [
                "A",
                "B",
                "C",
                "D"
            ],
            "correct_answer": "A",
            "question_type": "mcq",
            "difficulty": "expert"
        },
        headers=admin_headers
    )

    assert response.status_code == 422


def test_missing_question(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    quiz_id = create_quiz(
        client,
        admin_headers,
        category_id
    )

    response = client.post(
        QUESTION_URL + "/",
        json={
            "quiz_id": quiz_id,
            "options": [
                "A",
                "B",
                "C",
                "D"
            ],
            "correct_answer": "A",
            "question_type": "mcq",
            "difficulty": "easy"
        },
        headers=admin_headers
    )

    assert response.status_code == 422


def test_missing_options(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    quiz_id = create_quiz(
        client,
        admin_headers,
        category_id
    )

    response = client.post(
        QUESTION_URL + "/",
        json={
            "quiz_id": quiz_id,
            "question": "Question",
            "correct_answer": "A",
            "question_type": "mcq",
            "difficulty": "easy"
        },
        headers=admin_headers
    )

    assert response.status_code == 422


def test_missing_correct_answer(
    client,
    admin_headers
):

    category_id = create_category(
        client,
        admin_headers
    )

    quiz_id = create_quiz(
        client,
        admin_headers,
        category_id
    )

    response = client.post(
        QUESTION_URL + "/",
        json={
            "quiz_id": quiz_id,
            "question": "Question",
            "options": [
                "A",
                "B",
                "C",
                "D"
            ],
            "question_type": "mcq",
            "difficulty": "easy"
        },
        headers=admin_headers
    )

    assert response.status_code == 422


def test_get_questions_invalid_object_id(
    client,
    admin_headers
):

    response = client.get(
        f"{QUESTION_URL}/quiz/invalidid",
        headers=admin_headers
    )

    assert response.status_code == 404


def test_get_questions_without_token(
    client
):

    response = client.get(
        f"{QUESTION_URL}/quiz/689999999999999999999999"
    )

    assert response.status_code == 401


def test_create_question_without_token(
    client
):

    response = client.post(
        QUESTION_URL + "/",
        json={}
    )

    assert response.status_code == 401


def test_update_question_without_token(
    client
):

    response = client.put(
        f"{QUESTION_URL}/689999999999999999999999",
        json={}
    )

    assert response.status_code == 401


def test_delete_question_without_token(
    client
):

    response = client.delete(
        f"{QUESTION_URL}/689999999999999999999999"
    )

    assert response.status_code == 401