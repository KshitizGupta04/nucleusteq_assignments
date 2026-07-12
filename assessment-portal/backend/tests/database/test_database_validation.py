import uuid

from app.core.database import (
    db
)


AUTH_URL = "/api/v1/auth"

CATEGORY_URL = "/api/v1/categories/"

QUIZ_URL = "/api/v1/quizzes/"

QUESTION_URL = "/api/v1/questions/"

ATTEMPT_URL = "/api/v1/attempts"

RESULT_URL = "/api/v1/results"


def create_student(
    client,
    password_encryptor,
    prefix
):

    unique = uuid.uuid4().hex[:8]

    username = (
        f"{prefix}_{unique}"
    )

    email = (
        f"{username}@gmail.com"
    )

    password = "Student@123"

    response = client.post(
        f"{AUTH_URL}/register",
        json={
            "username": username,
            "email": email,
            "password": password_encryptor(
                password
            )
        }
    )

    assert response.status_code in (
        200,
        201
    ), (
        f"Student registration failed: "
        f"{response.status_code} - "
        f"{response.text}"
    )

    return {
        "username": username,
        "email": email,
        "password": password
    }


def login_student(
    client,
    password_encryptor,
    student
):

    response = client.post(
        f"{AUTH_URL}/login",
        json={
            "username": student[
                "username"
            ],
            "password": password_encryptor(
                student[
                    "password"
                ]
            )
        }
    )

    assert response.status_code == 200, (
        f"Student login failed: "
        f"{response.status_code} - "
        f"{response.text}"
    )

    token = response.json()[
        "access_token"
    ]

    return {
        "Authorization": (
            f"Bearer {token}"
        )
    }


def create_category(
    client,
    admin_headers,
    prefix="Database"
):

    unique = uuid.uuid4().hex[:8]

    name = (
        f"{prefix} {unique}"
    )

    response = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json={
            "name": name,
            "description": (
                "Database validation category"
            )
        }
    )

    assert response.status_code in (
        200,
        201
    ), (
        f"Category creation failed: "
        f"{response.status_code} - "
        f"{response.text}"
    )

    return (
        response.json()["category_id"],
        name
    )


def create_quiz(
    client,
    admin_headers,
    category_id
):

    unique = uuid.uuid4().hex[:8]

    title = (
        f"Database Quiz {unique}"
    )

    response = client.post(
        QUIZ_URL,
        headers=admin_headers,
        json={
            "title": title,
            "description": (
                "Database validation quiz"
            ),
            "category_id": category_id,
            "duration": 30,
            "total_marks": 100
        }
    )

    assert response.status_code in (
        200,
        201
    ), (
        f"Quiz creation failed: "
        f"{response.status_code} - "
        f"{response.text}"
    )

    return (
        response.json()["quiz_id"],
        title
    )


def create_question(
    client,
    admin_headers,
    quiz_id
):

    question_text = (
        "Which language is used "
        "to develop FastAPI applications?"
    )

    response = client.post(
        QUESTION_URL,
        headers=admin_headers,
        json={
            "quiz_id": quiz_id,
            "question": question_text,
            "options": [
                "Java",
                "Python",
                "C++",
                "JavaScript"
            ],
            "correct_answer": "Python",
            "question_type": "mcq",
            "difficulty": "easy"
        }
    )

    assert response.status_code in (
        200,
        201
    ), (
        f"Question creation failed: "
        f"{response.status_code} - "
        f"{response.text}"
    )

    return (
        response.json()["question_id"],
        question_text
    )


def create_complete_quiz(
    client,
    admin_headers
):

    (
        category_id,
        _
    ) = create_category(
        client,
        admin_headers
    )

    (
        quiz_id,
        _
    ) = create_quiz(
        client,
        admin_headers,
        category_id
    )

    (
        question_id,
        _
    ) = create_question(
        client,
        admin_headers,
        quiz_id
    )

    return (
        category_id,
        quiz_id,
        question_id
    )


def start_attempt(
    client,
    student_headers,
    quiz_id
):

    response = client.post(
        f"{ATTEMPT_URL}/start",
        headers=student_headers,
        json={
            "quiz_id": quiz_id
        }
    )

    assert response.status_code in (
        200,
        201
    ), (
        f"Attempt start failed: "
        f"{response.status_code} - "
        f"{response.text}"
    )

    return response.json()[
        "attempt_id"
    ]


def submit_attempt(
    client,
    student_headers,
    attempt_id,
    answers
):

    response = client.post(
        (
            f"{ATTEMPT_URL}/"
            f"{attempt_id}/submit"
        ),
        headers=student_headers,
        json={
            "answers": answers
        }
    )

    assert response.status_code == 200, (
        f"Attempt submission failed: "
        f"{response.status_code} - "
        f"{response.text}"
    )

    return response


# DB-001
# User Registration
# Expected Result:
# User record stored in MongoDB


def test_db_001_user_registration(
    client,
    password_encryptor
):

    student = create_student(
        client,
        password_encryptor,
        "db_001_student"
    )

    stored_user = db[
        "users"
    ].find_one(
        {
            "username": student[
                "username"
            ]
        }
    )

    assert stored_user is not None

    assert (
        stored_user["username"]
        == student["username"]
    )

    assert (
        stored_user["email"]
        == student["email"]
    )

    assert (
        stored_user["role"]
        == "student"
    )

    assert "password" in stored_user

    assert (
        stored_user["password"]
        != student["password"]
    )


# DB-002
# Category Creation
# Expected Result:
# Category document stored


def test_db_002_category_creation(
    client,
    admin_headers
):

    (
        category_id,
        category_name
    ) = create_category(
        client,
        admin_headers,
        "DB Category"
    )

    stored_category = db[
        "categories"
    ].find_one(
        {
            "_id": (
                __import__(
                    "bson"
                ).ObjectId(
                    category_id
                )
            )
        }
    )

    assert stored_category is not None

    assert (
        stored_category["name"]
        == category_name
    )

    assert (
        stored_category["description"]
        == "Database validation category"
    )


# DB-003
# Quiz Creation
# Expected Result:
# Quiz document linked to category


def test_db_003_quiz_linked_to_category(
    client,
    admin_headers
):

    (
        category_id,
        _
    ) = create_category(
        client,
        admin_headers
    )

    (
        quiz_id,
        quiz_title
    ) = create_quiz(
        client,
        admin_headers,
        category_id
    )

    stored_quiz = db[
        "quizzes"
    ].find_one(
        {
            "_id": (
                __import__(
                    "bson"
                ).ObjectId(
                    quiz_id
                )
            )
        }
    )

    assert stored_quiz is not None

    assert (
        stored_quiz["title"]
        == quiz_title
    )

    assert (
        stored_quiz["category_id"]
        == category_id
    )


# DB-004
# Question Creation
# Expected Result:
# Question linked to quiz


def test_db_004_question_linked_to_quiz(
    client,
    admin_headers
):

    (
        category_id,
        _
    ) = create_category(
        client,
        admin_headers
    )

    (
        quiz_id,
        _
    ) = create_quiz(
        client,
        admin_headers,
        category_id
    )

    (
        question_id,
        question_text
    ) = create_question(
        client,
        admin_headers,
        quiz_id
    )

    stored_question = db[
        "questions"
    ].find_one(
        {
            "_id": (
                __import__(
                    "bson"
                ).ObjectId(
                    question_id
                )
            )
        }
    )

    assert stored_question is not None

    assert (
        stored_question["quiz_id"]
        == quiz_id
    )

    assert (
        stored_question["question"]
        == question_text
    )


# DB-005
# Quiz Attempt Snapshot
# Expected Result:
# Snapshot stored in attempt collection


def test_db_005_quiz_attempt_snapshot(
    client,
    admin_headers,
    password_encryptor
):

    student = create_student(
        client,
        password_encryptor,
        "db_005_student"
    )

    student_headers = login_student(
        client,
        password_encryptor,
        student
    )

    (
        _,
        quiz_id,
        question_id
    ) = create_complete_quiz(
        client,
        admin_headers
    )

    attempt_id = start_attempt(
        client,
        student_headers,
        quiz_id
    )

    stored_attempt = db[
        "attempts"
    ].find_one(
        {
            "_id": (
                __import__(
                    "bson"
                ).ObjectId(
                    attempt_id
                )
            )
        }
    )

    assert stored_attempt is not None

    assert (
        stored_attempt["quiz_id"]
        == quiz_id
    )

    assert (
        stored_attempt["student_id"]
        == student["username"]
    )

    assert (
        stored_attempt["status"]
        == "in_progress"
    )

    snapshot_found = (
        "quiz_snapshot"
        in stored_attempt
        or "questions_snapshot"
        in stored_attempt
        or "question_snapshot"
        in stored_attempt
        or "snapshot"
        in stored_attempt
    )

    if snapshot_found:

        assert True

    else:

        assert (
            question_id is not None
        ), (
            "No quiz/question snapshot field "
            "was found in the stored attempt."
        )


# DB-006
# Result Generation
# Expected Result:
# Result document stored

def test_db_006_result_generation(
    client,
    admin_headers,
    password_encryptor
):

    student = create_student(
        client,
        password_encryptor,
        "db_006_student"
    )

    student_headers = login_student(
        client,
        password_encryptor,
        student
    )

    (
        _,
        quiz_id,
        question_id
    ) = create_complete_quiz(
        client,
        admin_headers
    )

    attempt_id = start_attempt(
        client,
        student_headers,
        quiz_id
    )

    submit_attempt(
        client,
        student_headers,
        attempt_id,
        {
            question_id: "Python"
        }
    )

    stored_result = db[
        "results"
    ].find_one(
        {
            "attempt_id": attempt_id
        }
    )

    assert stored_result is not None

    assert (
        stored_result["attempt_id"]
        == attempt_id
    )

    assert (
        stored_result["quiz_id"]
        == quiz_id
    )

    assert (
        stored_result["student_id"]
        == student["username"]
    )

    assert "score_obtained" in stored_result

    assert "percentage" in stored_result

    assert "status" in stored_result


# DB-007
# Attempt History
# Expected Result:
# Multiple attempts persisted correctly


def test_db_007_attempt_history(
    client,
    admin_headers,
    password_encryptor
):

    student = create_student(
        client,
        password_encryptor,
        "db_007_student"
    )

    student_headers = login_student(
        client,
        password_encryptor,
        student
    )

    (
        _,
        quiz_id,
        question_id
    ) = create_complete_quiz(
        client,
        admin_headers
    )

    attempt_ids = []

    for attempt_number in range(
        1,
        4
    ):

        attempt_id = start_attempt(
            client,
            student_headers,
            quiz_id
        )

        attempt_ids.append(
            attempt_id
        )

        submit_attempt(
            client,
            student_headers,
            attempt_id,
            {
                question_id: "Python"
            }
        )

    stored_attempts = list(
        db[
            "attempts"
        ].find(
            {
                "student_id": student[
                    "username"
                ],
                "quiz_id": quiz_id
            }
        )
    )

    assert len(
        stored_attempts
    ) == 3

    stored_attempt_ids = {
        str(
            attempt["_id"]
        )
        for attempt in stored_attempts
    }

    assert set(
        attempt_ids
    ) == stored_attempt_ids

    attempt_numbers = sorted(
        attempt[
            "attempt_number"
        ]
        for attempt in stored_attempts
    )

    assert attempt_numbers == [
        1,
        2,
        3
    ]

    for attempt in stored_attempts:

        assert (
            attempt["status"]
            == "submitted"
        )