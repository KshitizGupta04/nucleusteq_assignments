import uuid

ATTEMPT_URL = "/api/v1/attempts"
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
            "question": "What is Java Programming Language?",
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


def create_attempt(
    client,
    student_headers,
    quiz_id
):

    response = client.post(
        ATTEMPT_URL + "/start",
        json={
            "quiz_id": quiz_id
        },
        headers=student_headers
    )

    assert response.status_code == 200

    return response.json()["attempt_id"]


# ATT-001 Start Quiz Attempt
def test_att_001_start_attempt(
    client,
    admin_headers,
    student_headers
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

    response = client.post(
        ATTEMPT_URL + "/start",
        json={
            "quiz_id": quiz_id
        },
        headers=student_headers
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        ==
        "Attempt started successfully."
    )

#ATT-002 Save Answer
def test_att_002_save_answer(
    client,
    admin_headers,
    student_headers
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

    attempt_id = create_attempt(
        client,
        student_headers,
        quiz_id
    )

    response = client.put(
        f"{ATTEMPT_URL}/{attempt_id}/answer",
        json={
            "question_id": question_id,
            "answer": "Programming Language"
        },
        headers=student_headers
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        ==
        "Answer saved successfully."
    )

# ATT-003 Resume Attempt
def test_att_003_resume_attempt(
    client,
    admin_headers,
    student_headers
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

    attempt_id = create_attempt(
        client,
        student_headers,
        quiz_id
    )

    response = client.get(
        f"{ATTEMPT_URL}/{attempt_id}",
        headers=student_headers
    )

    assert response.status_code == 200

    assert (
        response.json()["attempt_id"]
        ==
        attempt_id
    )

    assert (
        response.json()["status"]
        ==
        "in_progress"
    )


#ATT-004 Submit Attempt
def test_att_004_submit_attempt(
    client,
    admin_headers,
    student_headers
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

    attempt_id = create_attempt(
        client,
        student_headers,
        quiz_id
    )

    response = client.post(
        f"{ATTEMPT_URL}/{attempt_id}/submit",
        json={
            "answers": {
                question_id:
                "Programming Language"
            }
        },
        headers=student_headers
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        ==
        "Attempt submitted successfully."
    )

# ATT-005 Maximum Three Attempts
def test_att_005_max_attempt_limit(
    client,
    admin_headers,
    student_headers
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

    for i in range(3):

        response = client.post(
            ATTEMPT_URL + "/start",
            json={
                "quiz_id": quiz_id
            },
            headers=student_headers
        )

        assert response.status_code == 200

        attempt_id = response.json()[
            "attempt_id"
        ]

        response = client.post(
            f"{ATTEMPT_URL}/{attempt_id}/submit",
            json={
                "answers": {
                    question_id:
                    "Programming Language"
                }
            },
            headers=student_headers
        )

        assert response.status_code == 200

    response = client.post(
        ATTEMPT_URL + "/start",
        json={
            "quiz_id": quiz_id
        },
        headers=student_headers
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        ==
        "Maximum attempts reached."
    )

# ATT-007 Invalid Quiz Id
def test_att_007_invalid_quiz(
    client,
    student_headers
):

    response = client.post(
        ATTEMPT_URL + "/start",
        json={
            "quiz_id":
            "invalid_quiz_id"
        },
        headers=student_headers
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        ==
        "Quiz not found."
    )

# ATT-008 Unauthorized Access
def test_att_008_without_token(
    client
):

    response = client.post(
        ATTEMPT_URL + "/start",
        json={
            "quiz_id":
            "123"
        }
    )

    assert response.status_code == 401


# Admin Cannot Start Attempt
def test_admin_cannot_start_attempt(
    client,
    admin_headers
):

    response = client.post(
        ATTEMPT_URL + "/start",
        json={
            "quiz_id":
            "123"
        },
        headers=admin_headers
    )

    assert response.status_code == 403


# Invalid Answer
def test_invalid_answer(
    client,
    admin_headers,
    student_headers
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

    attempt_id = create_attempt(
        client,
        student_headers,
        quiz_id
    )

    response = client.put(
        f"{ATTEMPT_URL}/{attempt_id}/answer",
        json={
            "question_id":
            question_id,
            "answer":
            "Wrong Option"
        },
        headers=student_headers
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        ==
        "Invalid answer selected."
    )


# Attempt Already Submitted
def test_attempt_already_submitted(
    client,
    admin_headers,
    student_headers
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

    attempt_id = create_attempt(
        client,
        student_headers,
        quiz_id
    )

    client.post(
        f"{ATTEMPT_URL}/{attempt_id}/submit",
        json={
            "answers": {
                question_id:
                "Programming Language"
            }
        },
        headers=student_headers
    )

    response = client.post(
        f"{ATTEMPT_URL}/{attempt_id}/submit",
        json={
            "answers": {
                question_id:
                "Programming Language"
            }
        },
        headers=student_headers
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        ==
        "Attempt has already been submitted."
    )



# Attempt Already In Progress
def test_attempt_already_in_progress(
    client,
    admin_headers,
    student_headers
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

    client.post(
        ATTEMPT_URL + "/start",
        json={
            "quiz_id":
            quiz_id
        },
        headers=student_headers
    )

    response = client.post(
        ATTEMPT_URL + "/start",
        json={
            "quiz_id":
            quiz_id
        },
        headers=student_headers
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        ==
        "You already have an ongoing attempt. Please submit it before starting a new attempt."
    )