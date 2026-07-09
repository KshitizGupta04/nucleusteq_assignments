import uuid


CATEGORY_URL = "/api/v1/categories"
QUIZ_URL = "/api/v1/quizzes"
QUESTION_URL = "/api/v1/questions"
ATTEMPT_URL = "/api/v1/attempts"
RESULT_URL = "/api/v1/results"


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
            "description": "Java Programming Quiz",
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
    quiz_id,
    question_text,
    correct_answer
):

    response = client.post(
        QUESTION_URL + "/",
        json={
            "quiz_id": quiz_id,
            "question": question_text,
            "options": [
                correct_answer,
                "Wrong Option 1",
                "Wrong Option 2",
                "Wrong Option 3"
            ],
            "correct_answer": correct_answer,
            "question_type": "mcq",
            "difficulty": "easy"
        },
        headers=admin_headers
    )

    assert response.status_code == 200

    return response.json()["question_id"]


def create_quiz_with_questions(
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

    question_1 = create_question(
        client,
        admin_headers,
        quiz_id,
        "Which keyword is used for inheritance in Java?",
        "extends"
    )

    question_2 = create_question(
        client,
        admin_headers,
        quiz_id,
        "Which collection does not allow duplicates?",
        "Set"
    )

    question_3 = create_question(
        client,
        admin_headers,
        quiz_id,
        "Which method is the entry point of Java?",
        "main()"
    )

    question_4 = create_question(
        client,
        admin_headers,
        quiz_id,
        "Which exception is unchecked in Java?",
        "RuntimeException"
    )

    return (
        quiz_id,
        question_1,
        question_2,
        question_3,
        question_4
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

    return response.json()["attempt_id"]


def submit_attempt(
    client,
    student_headers,
    attempt_id,
    answers
):

    response = client.post(
        f"{ATTEMPT_URL}/{attempt_id}/submit",
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


# RES-001 Generate Result
# Expected: Result is generated after attempt submission
def test_res_001_generate_result(
    client,
    admin_headers,
    student_headers
):

    (
        quiz_id,
        question_1,
        question_2,
        question_3,
        question_4
    ) = create_quiz_with_questions(
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
            question_1: "extends",
            question_2: "Set",
            question_3: "main()",
            question_4: "RuntimeException"
        }
    )

    result = get_latest_result(
        client,
        student_headers
    )

    assert result["attempt_id"] == attempt_id

    assert result["quiz_id"] == quiz_id

    assert result["score_obtained"] == 100

    assert result["total_marks"] == 100

    assert result["percentage"] == 100

    assert result["status"] == "pass"


# RES-002 Calculate Percentage
# Input: 75 marks out of 100
# Expected: Percentage = 75%
def test_res_002_calculate_percentage(
    client,
    admin_headers,
    student_headers
):

    (
        quiz_id,
        question_1,
        question_2,
        question_3,
        question_4
    ) = create_quiz_with_questions(
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
            question_1: "extends",
            question_2: "Set",
            question_3: "main()",
            question_4: "Wrong Option 1"
        }
    )

    result = get_latest_result(
        client,
        student_headers
    )

    assert result["score_obtained"] == 75

    assert result["total_marks"] == 100

    assert result["percentage"] == 75


# RES-003 Pass / Fail Validation
# Expected:
# Percentage >= 40 -> pass
# Percentage < 40 -> fail
def test_res_003_pass_validation(
    client,
    admin_headers,
    student_headers
):

    (
        quiz_id,
        question_1,
        question_2,
        question_3,
        question_4
    ) = create_quiz_with_questions(
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
            question_1: "extends",
            question_2: "Set",
            question_3: "main()",
            question_4: "Wrong Option 1"
        }
    )

    result = get_latest_result(
        client,
        student_headers
    )

    assert result["percentage"] == 75

    assert result["status"] == "pass"


def test_res_003_fail_validation(
    client,
    admin_headers,
    student_headers
):

    (
        quiz_id,
        question_1,
        question_2,
        question_3,
        question_4
    ) = create_quiz_with_questions(
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
            question_1: "extends",
            question_2: "Wrong Option 1",
            question_3: "Wrong Option 1",
            question_4: "Wrong Option 1"
        }
    )

    result = get_latest_result(
        client,
        student_headers
    )

    assert result["percentage"] == 25

    assert result["status"] == "fail"


# RES-004 Fetch Student Results
# Expected: Student receives their result history
def test_res_004_fetch_student_results(
    client,
    admin_headers,
    student_headers
):

    (
        quiz_id,
        question_1,
        question_2,
        question_3,
        question_4
    ) = create_quiz_with_questions(
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
            question_1: "extends",
            question_2: "Set",
            question_3: "main()",
            question_4: "RuntimeException"
        }
    )

    response = client.get(
        RESULT_URL + "/me",
        headers=student_headers
    )

    assert response.status_code == 200

    results = response.json()

    assert len(results) > 0

    assert results[0]["attempt_id"] == attempt_id

    assert results[0]["quiz_id"] == quiz_id


# RES-005 Fetch Admin Dashboard Results
# Expected: Admin receives all results
def test_res_005_fetch_admin_dashboard_results(
    client,
    admin_headers,
    student_headers
):

    (
        quiz_id,
        question_1,
        question_2,
        question_3,
        question_4
    ) = create_quiz_with_questions(
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
            question_1: "extends",
            question_2: "Set",
            question_3: "main()",
            question_4: "RuntimeException"
        }
    )

    response = client.get(
        RESULT_URL + "/admin/dashboard",
        headers=admin_headers
    )

    assert response.status_code == 200

    results = response.json()

    assert len(results) > 0

    result = next(
        (
            item
            for item in results
            if item["attempt_id"] == attempt_id
        ),
        None
    )

    assert result is not None

    assert result["quiz_id"] == quiz_id

    assert result["score_obtained"] == 100

    assert result["percentage"] == 100

    assert result["status"] == "pass"


# RES-006 Result Breakdown
# Expected: Per-question score breakdown is returned
def test_res_006_result_breakdown(
    client,
    admin_headers,
    student_headers
):

    (
        quiz_id,
        question_1,
        question_2,
        question_3,
        question_4
    ) = create_quiz_with_questions(
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
            question_1: "extends",
            question_2: "Set",
            question_3: "main()",
            question_4: "Wrong Option 1"
        }
    )

    result = get_latest_result(
        client,
        student_headers
    )

    result_id = result[
        "result_id"
    ]

    response = client.get(
        f"{RESULT_URL}/{result_id}/breakdown",
        headers=student_headers
    )

    assert response.status_code == 200

    breakdown = response.json()

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


# Student Cannot Access Admin Dashboard
# Authorization validation
def test_student_cannot_access_admin_dashboard(
    client,
    student_headers
):

    response = client.get(
        RESULT_URL + "/admin/dashboard",
        headers=student_headers
    )

    assert response.status_code == 403


# Result API Without Authentication
# Expected: 401 Unauthorized
def test_result_without_authentication(
    client
):

    response = client.get(
        RESULT_URL + "/me"
    )

    assert response.status_code == 401


# Expected: 404 Result Not Found
def test_invalid_result_id(
    client,
    student_headers
):

    response = client.get(
        RESULT_URL + "/invalid_result_id",
        headers=student_headers
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        ==
        "Result not found."
    )