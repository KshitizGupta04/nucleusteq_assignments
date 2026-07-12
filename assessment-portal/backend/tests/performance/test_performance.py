import time
import uuid

from concurrent.futures import (
    ThreadPoolExecutor
)


AUTH_URL = "/api/v1/auth"

CATEGORY_URL = "/api/v1/categories/"

QUIZ_URL = "/api/v1/quizzes/"

QUESTION_URL = "/api/v1/questions/"

ATTEMPT_URL = "/api/v1/attempts"

RESULT_URL = "/api/v1/results"


CONCURRENT_USERS = 20

MAX_RESPONSE_TIME = 2.0


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

    register_response = client.post(
        f"{AUTH_URL}/register",
        json={
            "username": username,
            "email": email,
            "password": password_encryptor(
                password
            )
        }
    )

    assert register_response.status_code in (
        200,
        201
    ), (
        f"Student registration failed: "
        f"{register_response.status_code} - "
        f"{register_response.text}"
    )

    return {
        "username": username,
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
    admin_headers
):

    unique = uuid.uuid4().hex[:8]

    response = client.post(
        CATEGORY_URL,
        headers=admin_headers,
        json={
            "name": (
                f"Performance {unique}"
            ),
            "description": (
                "Performance test category"
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
                f"Performance Quiz {unique}"
            ),
            "description": (
                "Performance testing quiz"
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

    return response.json()[
        "quiz_id"
    ]


def create_question(
    client,
    admin_headers,
    quiz_id
):

    response = client.post(
        QUESTION_URL,
        headers=admin_headers,
        json={
            "quiz_id": quiz_id,
            "question": (
                "Which language is used "
                "for FastAPI development?"
            ),
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


# PERF-001
# Login Response Time
# Input: 20 Concurrent Users
# Expected Result: Less Than 2 Seconds


def test_perf_001_login_response_time(
    client,
    password_encryptor
):

    students = []

    for index in range(
        CONCURRENT_USERS
    ):

        student = create_student(
            client,
            password_encryptor,
            f"perf_001_{index}"
        )

        students.append(
            student
        )

    def login_request(
        student
    ):

        encrypted_password = (
            password_encryptor(
                student[
                    "password"
                ]
            )
        )

        start_time = (
            time.perf_counter()
        )

        response = client.post(
            f"{AUTH_URL}/login",
            json={
                "username": student[
                    "username"
                ],
                "password": encrypted_password
            }
        )

        elapsed_time = (
            time.perf_counter()
            - start_time
        )

        return (
            response.status_code,
            elapsed_time
        )

    with ThreadPoolExecutor(
        max_workers=CONCURRENT_USERS
    ) as executor:

        results = list(
            executor.map(
                login_request,
                students
            )
        )

    status_codes = [
        status_code
        for (
            status_code,
            _
        ) in results
    ]

    response_times = [
        elapsed_time
        for (
            _,
            elapsed_time
        ) in results
    ]

    slowest_response = max(
        response_times
    )

    average_response = (
        sum(
            response_times
        )
        / len(
            response_times
        )
    )

    print(
        "\nPERF-001 Login Performance:"
    )

    print(
        f"Concurrent users: "
        f"{CONCURRENT_USERS}"
    )

    print(
        f"Average response time: "
        f"{average_response:.4f}s"
    )

    print(
        f"Slowest response time: "
        f"{slowest_response:.4f}s"
    )

    assert all(
        status_code == 200
        for status_code in status_codes
    ), (
        "One or more login requests failed."
    )

    assert (
        slowest_response
        < MAX_RESPONSE_TIME
    ), (
        "Login API exceeded "
        f"{MAX_RESPONSE_TIME} seconds. "
        f"Slowest response: "
        f"{slowest_response:.4f}s. "
        f"Average response: "
        f"{average_response:.4f}s."
    )


# PERF-002
# Fetch Quiz Questions
# Input: 20 Concurrent Users
# Expected Result: Less Than 2 Seconds


def test_perf_002_fetch_quiz_questions(
    client,
    admin_headers,
    password_encryptor
):

    (
        _,
        quiz_id,
        _
    ) = create_complete_quiz(
        client,
        admin_headers
    )

    students = []

    for index in range(
        CONCURRENT_USERS
    ):

        student = create_student(
            client,
            password_encryptor,
            f"perf_002_{index}"
        )

        headers = login_student(
            client,
            password_encryptor,
            student
        )

        students.append(
            headers
        )

    def fetch_questions(
        student_headers
    ):

        start_time = (
            time.perf_counter()
        )

        response = client.get(
            (
                f"{QUESTION_URL}"
                f"quiz/{quiz_id}"
            ),
            headers=student_headers
        )

        elapsed_time = (
            time.perf_counter()
            - start_time
        )

        return (
            response.status_code,
            elapsed_time
        )

    with ThreadPoolExecutor(
        max_workers=CONCURRENT_USERS
    ) as executor:

        results = list(
            executor.map(
                fetch_questions,
                students
            )
        )

    for (
        status_code,
        elapsed_time
    ) in results:

        assert status_code == 200

        assert (
            elapsed_time
            < MAX_RESPONSE_TIME
        ), (
            "Fetch questions API exceeded "
            f"{MAX_RESPONSE_TIME} seconds. "
            f"Actual: {elapsed_time:.4f}s"
        )


# PERF-003
# Submit Quiz
# Input: 20 Concurrent Users
# Expected Result: Successful Submission


def test_perf_003_submit_quiz(
    client,
    admin_headers,
    password_encryptor
):

    (
        _,
        quiz_id,
        question_id
    ) = create_complete_quiz(
        client,
        admin_headers
    )

    attempts = []

    for index in range(
        CONCURRENT_USERS
    ):

        student = create_student(
            client,
            password_encryptor,
            f"perf_003_{index}"
        )

        headers = login_student(
            client,
            password_encryptor,
            student
        )

        attempt_id = start_attempt(
            client,
            headers,
            quiz_id
        )

        attempts.append(
            (
                headers,
                attempt_id
            )
        )

    def submit_quiz(
        attempt_data
    ):

        (
            headers,
            attempt_id
        ) = attempt_data

        response = client.post(
            (
                f"{ATTEMPT_URL}/"
                f"{attempt_id}/submit"
            ),
            headers=headers,
            json={
                "answers": {
                    question_id: "Python"
                }
            }
        )

        return response.status_code

    with ThreadPoolExecutor(
        max_workers=CONCURRENT_USERS
    ) as executor:

        results = list(
            executor.map(
                submit_quiz,
                attempts
            )
        )

    for status_code in results:

        assert status_code == 200


# PERF-004
# Generate Results
# Input: 20 Concurrent Users
# Expected Result:
# Results Generated Successfully


def test_perf_004_generate_results(
    client,
    admin_headers,
    password_encryptor
):

    (
        _,
        quiz_id,
        question_id
    ) = create_complete_quiz(
        client,
        admin_headers
    )

    students = []

    for index in range(
        CONCURRENT_USERS
    ):

        student = create_student(
            client,
            password_encryptor,
            f"perf_004_{index}"
        )

        headers = login_student(
            client,
            password_encryptor,
            student
        )

        attempt_id = start_attempt(
            client,
            headers,
            quiz_id
        )

        students.append(
            (
                headers,
                attempt_id
            )
        )

    def submit_and_generate_result(
        student_data
    ):

        (
            headers,
            attempt_id
        ) = student_data

        submit_response = client.post(
            (
                f"{ATTEMPT_URL}/"
                f"{attempt_id}/submit"
            ),
            headers=headers,
            json={
                "answers": {
                    question_id: "Python"
                }
            }
        )

        if (
            submit_response.status_code
            != 200
        ):

            return False

        results_response = client.get(
            f"{RESULT_URL}/me",
            headers=headers
        )

        if (
            results_response.status_code
            != 200
        ):

            return False

        results = (
            results_response.json()
        )

        return any(
            result["attempt_id"]
            == attempt_id
            for result in results
        )

    with ThreadPoolExecutor(
        max_workers=CONCURRENT_USERS
    ) as executor:

        results = list(
            executor.map(
                submit_and_generate_result,
                students
            )
        )

    assert all(
        results
    ), (
        "Results were not generated "
        "successfully for all "
        "20 concurrent users."
    )