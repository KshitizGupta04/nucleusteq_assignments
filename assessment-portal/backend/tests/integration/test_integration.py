import uuid

from tests.conftest import (
    encrypt_password
)


CATEGORY_URL = "/api/v1/categories"
QUIZ_URL = "/api/v1/quizzes"
QUESTION_URL = "/api/v1/questions"
ATTEMPT_URL = "/api/v1/attempts"
RESULT_URL = "/api/v1/results"
AUTH_URL = "/api/v1/auth"


def create_student(
    client,
    prefix="integration_student"
):

    unique = uuid.uuid4().hex[:8]

    username = (
        f"{prefix}_{unique}"
    )

    email = (
        f"{prefix}_{unique}"
        "@gmail.com"
    )

    password = "Student@123"

    register_response = client.post(
        AUTH_URL + "/register",
        json={
            "username": username,
            "email": email,
            "password": encrypt_password(
                password
            )
        }
    )

    assert register_response.status_code in (
        200,
        201
    )

    login_response = client.post(
        AUTH_URL + "/login",
        json={
            "username": username,
            "password": encrypt_password(
                password
            )
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()[
        "access_token"
    ]

    headers = {
        "Authorization": (
            f"Bearer {token}"
        )
    }

    return (
        username,
        headers
    )


def create_category(
    client,
    admin_headers
):

    unique = uuid.uuid4().hex[:8]

    response = client.post(
        CATEGORY_URL + "/",
        json={
            "name": (
                f"Integration_Category_"
                f"{unique}"
            ),
            "description": (
                "Category for integration testing"
            )
        },
        headers=admin_headers
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
        QUIZ_URL + "/",
        json={
            "title": (
                f"Integration_Quiz_"
                f"{unique}"
            ),
            "description": (
                "Quiz for integration testing"
            ),
            "category_id": category_id,
            "duration": 30,
            "total_marks": 100
        },
        headers=admin_headers
    )

    assert response.status_code == 200

    return response.json()[
        "quiz_id"
    ]


def create_question(
    client,
    admin_headers,
    quiz_id,
    question_text=(
        "Which language is platform independent?"
    ),
    correct_answer="Java"
):

    response = client.post(
        QUESTION_URL + "/",
        json={
            "quiz_id": quiz_id,
            "question": question_text,
            "options": [
                correct_answer,
                "C",
                "HTML",
                "CSS"
            ],
            "correct_answer": correct_answer,
            "question_type": "mcq",
            "difficulty": "easy"
        },
        headers=admin_headers
    )

    assert response.status_code == 200

    return response.json()[
        "question_id"
    ]


def create_complete_quiz(
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
        ATTEMPT_URL + "/start",
        json={
            "quiz_id": quiz_id
        },
        headers=student_headers
    )

    assert response.status_code == 200

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
        json={
            "answers": answers
        },
        headers=student_headers
    )

    assert response.status_code == 200

    return response


def get_latest_result(
    client,
    student_headers
):

    response = client.get(
        RESULT_URL + "/me",
        headers=student_headers
    )

    assert response.status_code == 200

    results = response.json()

    assert len(results) > 0

    return results[0]


# SRS INTEGRATION TEST CASES


# INT-001
# Register -> Login -> Start Attempt
# -> Submit -> Result Generated


def test_int_001_complete_student_flow(
    client,
    admin_headers
):

    (
        _,
        student_headers
    ) = create_student(
        client,
        "int_001_student"
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

    submit_response = submit_attempt(
        client,
        student_headers,
        attempt_id,
        {
            question_id: "Java"
        }
    )

    assert (
        submit_response.json()["message"]
        == "Attempt submitted successfully."
    )

    result = get_latest_result(
        client,
        student_headers
    )

    assert (
        result["attempt_id"]
        == attempt_id
    )

    assert (
        result["quiz_id"]
        == quiz_id
    )

    assert (
        result["score_obtained"]
        == 100
    )

    assert (
        result["total_marks"]
        == 100
    )

    assert (
        result["percentage"]
        == 100
    )

    assert (
        result["status"]
        == "pass"
    )


# INT-002
# Admin Creates Category -> Quiz
# -> Question -> Student Attempts Quiz


def test_int_002_admin_to_student_flow(
    client,
    admin_headers
):

    (
        _,
        student_headers
    ) = create_student(
        client,
        "int_002_student"
    )

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

    attempt_id = start_attempt(
        client,
        student_headers,
        quiz_id
    )

    resume_response = client.get(
        f"{ATTEMPT_URL}/{attempt_id}",
        headers=student_headers
    )

    assert resume_response.status_code == 200

    attempt_data = resume_response.json()

    assert (
        attempt_data["quiz_id"]
        == quiz_id
    )

    assert (
        len(
            attempt_data[
                "question_snapshot"
            ]
        )
        == 1
    )

    assert (
        attempt_data[
            "question_snapshot"
        ][0]["id"]
        == question_id
    )

    submit_attempt(
        client,
        student_headers,
        attempt_id,
        {
            question_id: "Java"
        }
    )

    result = get_latest_result(
        client,
        student_headers
    )

    assert result["quiz_id"] == quiz_id

    assert result["attempt_id"] == attempt_id


# INT-003
# Maximum Attempt Limit Enforcement


def test_int_003_maximum_attempt_limit(
    client,
    admin_headers
):

    (
        _,
        student_headers
    ) = create_student(
        client,
        "int_003_student"
    )

    (
        _,
        quiz_id,
        question_id
    ) = create_complete_quiz(
        client,
        admin_headers
    )

    for attempt_number in range(
        1,
        4
    ):

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
                question_id: "Java"
            }
        )

    fourth_attempt_response = client.post(
        ATTEMPT_URL + "/start",
        json={
            "quiz_id": quiz_id
        },
        headers=student_headers
    )

    assert (
        fourth_attempt_response.status_code
        == 400
    )


# INT-004
# Result Calculation Consistency


def test_int_004_result_calculation_consistency(
    client,
    admin_headers
):

    (
        _,
        student_headers
    ) = create_student(
        client,
        "int_004_student"
    )

    category_id = create_category(
        client,
        admin_headers
    )

    quiz_id = create_quiz(
        client,
        admin_headers,
        category_id
    )

    question_1 = create_question(
        client,
        admin_headers,
        quiz_id,
        (
            "Which keyword is used for "
            "inheritance in Java?"
        ),
        "extends"
    )

    question_2 = create_question(
        client,
        admin_headers,
        quiz_id,
        (
            "Which collection does not "
            "allow duplicates?"
        ),
        "Set"
    )

    question_3 = create_question(
        client,
        admin_headers,
        quiz_id,
        (
            "Which method is the entry "
            "point of Java?"
        ),
        "main()"
    )

    question_4 = create_question(
        client,
        admin_headers,
        quiz_id,
        (
            "Which exception is unchecked "
            "in Java?"
        ),
        "RuntimeException"
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
            question_1: "extends",
            question_2: "Set",
            question_3: "main()",
            question_4: "C"
        }
    )

    result = get_latest_result(
        client,
        student_headers
    )

    assert result["score_obtained"] == 75

    assert result["total_marks"] == 100

    assert result["percentage"] == 75

    assert result["status"] == "pass"

    result_id = result[
        "result_id"
    ]

    breakdown_response = client.get(
        (
            f"{RESULT_URL}/"
            f"{result_id}/breakdown"
        ),
        headers=student_headers
    )

    assert (
        breakdown_response.status_code
        == 200
    )

    breakdown = (
        breakdown_response.json()
    )

    assert len(breakdown) == 4

    correct_answers = [
        question
        for question in breakdown
        if question["is_correct"] is True
    ]

    incorrect_answers = [
        question
        for question in breakdown
        if question["is_correct"] is False
    ]

    assert len(correct_answers) == 3

    assert len(incorrect_answers) == 1

    assert sum(
        question["marks_obtained"]
        for question in breakdown
    ) == 75


# INT-005
# Student A Cannot Access
# Student B's Result


def test_int_005_student_result_isolation(
    client,
    admin_headers
):

    (
        _,
        student_a_headers
    ) = create_student(
        client,
        "int_005_student_a"
    )

    (
        _,
        student_b_headers
    ) = create_student(
        client,
        "int_005_student_b"
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
        student_b_headers,
        quiz_id
    )

    submit_attempt(
        client,
        student_b_headers,
        attempt_id,
        {
            question_id: "Java"
        }
    )

    student_b_result = get_latest_result(
        client,
        student_b_headers
    )

    assert (
        student_b_result["attempt_id"]
        == attempt_id
    )

    assert (
        student_b_result["quiz_id"]
        == quiz_id
    )

    result_id = student_b_result[
        "result_id"
    ]

    student_a_response = client.get(
        f"{RESULT_URL}/{result_id}",
        headers=student_a_headers
    )

    assert (
        student_a_response.status_code
        in (
            403,
            404
        )
    )

    student_a_results_response = client.get(
        RESULT_URL + "/me",
        headers=student_a_headers
    )

    assert (
        student_a_results_response.status_code
        == 200
    )

    student_a_results = (
        student_a_results_response.json()
    )

    assert all(
        result["result_id"]
        != result_id
        for result in student_a_results
    )