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



# EXT-002
# Test-Level Average Score and Pass Rate
# Expected Result:
# Admin can view aggregated statistics for
# a quiz including average score, pass rate,
# pass count, fail count and total attempts.
def test_ext_002_test_level_average_score_and_pass_rate(
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
        (
            f"{RESULT_URL}/admin/quiz/"
            f"{quiz_id}/statistics"
        ),
        headers=admin_headers
    )


    assert response.status_code == 200


    data = response.json()


    assert data[
        "quiz_id"
    ] == quiz_id


    assert data[
        "total_attempts"
    ] == 1


    assert data[
        "average_score"
    ] == 100.0


    assert data[
        "pass_count"
    ] == 1


    assert data[
        "fail_count"
    ] == 0


    assert data[
        "pass_rate"
    ] == 100.0



# EXT-003
# Leaderboard Per Test
# Expected Result:
# Admin can view the leaderboard for a quiz.
# Students are ranked by percentage, and
# only the best attempt of each student is
# included in the leaderboard.
def test_ext_003_leaderboard_per_test(
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
        (
            f"{RESULT_URL}/admin/quiz/"
            f"{quiz_id}/leaderboard"
        ),
        headers=admin_headers
    )


    assert response.status_code == 200


    data = response.json()


    assert len(
        data
    ) == 1


    leaderboard_entry = data[
        0
    ]


    assert leaderboard_entry[
        "rank"
    ] == 1


    assert leaderboard_entry[
        "student_id"
    ] == "test_student_category"


    assert leaderboard_entry[
        "score_obtained"
    ] == 100.0


    assert leaderboard_entry[
        "total_marks"
    ] == 100.0


    assert leaderboard_entry[
        "percentage"
    ] == 100.0



# EXT-004: Verify short answer question type with
# case-insensitive and whitespace-tolerant evaluation.
def test_ext_004_short_answer_question_type(
    client,
    admin_headers,
    student_headers
):

    category_response = client.post(
        "/api/v1/categories",
        json={
            "name": "EXT-004 Category",
            "description": (
                "Category for testing "
                "short answer questions."
            )
        },
        headers=admin_headers
    )

    assert category_response.status_code in [
        200,
        201
    ]

    category_id = category_response.json()[
        "category_id"
    ]


    quiz_response = client.post(
        "/api/v1/quizzes",
        json={
            "title": "EXT-004 Quiz",
            "description": (
                "Quiz for testing short "
                "answer question support."
            ),
            "category_id": category_id,
            "duration": 30,
            "total_marks": 100
        },
        headers=admin_headers
    )

    assert quiz_response.status_code in [
        200,
        201
    ]

    quiz_id = quiz_response.json()[
        "quiz_id"
    ]


    question_response = client.post(
        "/api/v1/questions",
        json={
            "quiz_id": quiz_id,
            "question": (
                "What does JVM stand for?"
            ),
            "options": [],
            "correct_answer": (
                "Java Virtual Machine"
            ),
            "question_type": "short_answer",
            "difficulty": "easy"
        },
        headers=admin_headers
    )

    assert question_response.status_code in [
        200,
        201
    ]

    question_id = question_response.json()[
        "question_id"
    ]


    attempt_response = client.post(
        "/api/v1/attempts/start",
        json={
            "quiz_id": quiz_id
        },
        headers=student_headers
    )

    assert attempt_response.status_code in [
        200,
        201
    ]

    attempt_id = attempt_response.json()[
        "attempt_id"
    ]


    submit_response = client.post(
        (
            f"/api/v1/attempts/"
            f"{attempt_id}/submit"
        ),
        json={
            "answers": {
                question_id: (
                    "  java virtual machine  "
                )
            }
        },
        headers=student_headers
    )

    assert submit_response.status_code == 200


    results_response = client.get(
        "/api/v1/results/me",
        headers=student_headers
    )

    assert results_response.status_code == 200

    results = results_response.json()

    matching_result = next(
        result
        for result in results
        if result["attempt_id"] == attempt_id
    )


    assert matching_result[
        "score_obtained"
    ] == 100.0

    assert matching_result[
        "percentage"
    ] == 100.0

    assert matching_result[
        "status"
    ] == "pass"


    result_id = matching_result[
        "result_id"
    ]


    breakdown_response = client.get(
        (
            f"/api/v1/results/"
            f"{result_id}/breakdown"
        ),
        headers=student_headers
    )

    assert breakdown_response.status_code == 200

    breakdown = breakdown_response.json()


    assert len(breakdown) == 1

    assert breakdown[0][
        "selected_answer"
    ] == "  java virtual machine  "

    assert breakdown[0][
        "correct_answer"
    ] == "Java Virtual Machine"

    assert breakdown[0][
        "is_correct"
    ] is True

    assert breakdown[0][
        "marks_obtained"
    ] == 100.0

# EXT-006: Verify negative marking for wrong answers.
def test_ext_006_negative_marking(
    client,
    admin_headers,
    student_headers
):

    category_response = client.post(
        "/api/v1/categories",
        json={
            "name": "EXT-006 Category",
            "description": (
                "Category for testing "
                "negative marking."
            )
        },
        headers=admin_headers
    )

    assert category_response.status_code in [
        200,
        201
    ]

    category_id = category_response.json()[
        "category_id"
    ]


    quiz_response = client.post(
        "/api/v1/quizzes",
        json={
            "title": "EXT-006 Quiz",
            "description": (
                "Quiz for testing "
                "negative marking."
            ),
            "category_id": category_id,
            "duration": 30,
            "total_marks": 100,
            "negative_marks": 5
        },
        headers=admin_headers
    )

    assert quiz_response.status_code in [
        200,
        201
    ]

    quiz_id = quiz_response.json()[
        "quiz_id"
    ]


    for index in range(
        1,
        5
    ):

        question_response = client.post(
            "/api/v1/questions",
            json={
                "quiz_id": quiz_id,
                "question": (
                    f"EXT-006 question "
                    f"number {index}?"
                ),
                "options": [
                    f"Correct {index}",
                    f"Wrong A {index}",
                    f"Wrong B {index}",
                    f"Wrong C {index}"
                ],
                "correct_answer": (
                    f"Correct {index}"
                ),
                "question_type": "mcq",
                "difficulty": "easy"
            },
            headers=admin_headers
        )

        assert question_response.status_code in [
            200,
            201
        ]


    attempt_response = client.post(
        "/api/v1/attempts/start",
        json={
            "quiz_id": quiz_id
        },
        headers=student_headers
    )

    assert attempt_response.status_code in [
        200,
        201
    ]

    attempt_id = attempt_response.json()[
        "attempt_id"
    ]


    resume_response = client.get(
        (
            f"/api/v1/attempts/"
            f"{attempt_id}"
        ),
        headers=student_headers
    )

    assert resume_response.status_code == 200

    questions = resume_response.json()[
        "question_snapshot"
    ]

    assert len(questions) == 4


    first_question = questions[0]

    second_question = questions[1]

    third_question = questions[2]


    answers = {
        first_question["id"]:
            first_question["options"][0],

        second_question["id"]:
            second_question["options"][0],

        third_question["id"]:
            third_question["options"][1]
    }


    submit_response = client.post(
        (
            f"/api/v1/attempts/"
            f"{attempt_id}/submit"
        ),
        json={
            "answers": answers
        },
        headers=student_headers
    )

    assert submit_response.status_code == 200


    results_response = client.get(
        "/api/v1/results/me",
        headers=student_headers
    )

    assert results_response.status_code == 200

    matching_results = [
        result
        for result in results_response.json()
        if result["attempt_id"] == attempt_id
    ]

    assert len(matching_results) == 1

    result = matching_results[0]


    assert result[
        "score_obtained"
    ] == 45.0

    assert result[
        "percentage"
    ] == 45.0

    assert result[
        "status"
    ] == "pass"


    result_id = result[
        "result_id"
    ]


    breakdown_response = client.get(
        (
            f"/api/v1/results/"
            f"{result_id}/breakdown"
        ),
        headers=student_headers
    )

    assert breakdown_response.status_code == 200

    breakdown = breakdown_response.json()


    correct_questions = [
        question
        for question in breakdown
        if question["is_correct"] is True
    ]

    wrong_questions = [
        question
        for question in breakdown
        if (
            question["selected_answer"]
            is not None
            and question["is_correct"] is False
        )
    ]

    unanswered_questions = [
        question
        for question in breakdown
        if question["selected_answer"] is None
    ]


    assert len(correct_questions) == 2

    assert len(wrong_questions) == 1

    assert len(unanswered_questions) == 1


    for question in correct_questions:

        assert question[
            "marks_obtained"
        ] == 25.0


    assert wrong_questions[0][
        "marks_obtained"
    ] == -5.0


    assert unanswered_questions[0][
        "marks_obtained"
    ] == 0.0

# EXT-005: Verify random selection of a configured number
# of questions from a larger question pool.
def test_ext_005_question_pool_random_selection(
    client,
    admin_headers,
    student_headers
):

    category_response = client.post(
        "/api/v1/categories",
        json={
            "name": "EXT-005 Category",
            "description": (
                "Category for testing random "
                "question pool selection."
            )
        },
        headers=admin_headers
    )

    assert category_response.status_code in [
        200,
        201
    ]

    category_id = category_response.json()[
        "category_id"
    ]


    quiz_response = client.post(
        "/api/v1/quizzes",
        json={
            "title": "EXT-005 Quiz",
            "description": (
                "Quiz for testing random "
                "question pool selection."
            ),
            "category_id": category_id,
            "duration": 30,
            "total_marks": 100,
            "question_count": 3
        },
        headers=admin_headers
    )

    assert quiz_response.status_code in [
        200,
        201
    ]

    quiz_id = quiz_response.json()[
        "quiz_id"
    ]


    for index in range(
        1,
        6
    ):

        question_response = client.post(
            "/api/v1/questions",
            json={
                "quiz_id": quiz_id,
                "question": (
                    f"EXT-005 question number "
                    f"{index}?"
                ),
                "options": [
                    f"Option A {index}",
                    f"Option B {index}",
                    f"Option C {index}",
                    f"Option D {index}"
                ],
                "correct_answer": (
                    f"Option A {index}"
                ),
                "question_type": "mcq",
                "difficulty": "easy"
            },
            headers=admin_headers
        )

        assert question_response.status_code in [
            200,
            201
        ]


    attempt_response = client.post(
        "/api/v1/attempts/start",
        json={
            "quiz_id": quiz_id
        },
        headers=student_headers
    )

    assert attempt_response.status_code in [
        200,
        201
    ]

    attempt_id = attempt_response.json()[
        "attempt_id"
    ]


    resume_response = client.get(
        (
            f"/api/v1/attempts/"
            f"{attempt_id}"
        ),
        headers=student_headers
    )

    assert resume_response.status_code == 200

    attempt_data = resume_response.json()

    questions = attempt_data[
        "question_snapshot"
    ]


    assert len(questions) == 3

    question_ids = [
        question["id"]
        for question in questions
    ]

    assert len(
        set(question_ids)
    ) == 3


    for question in questions:

        assert question[
            "quiz_id"
        ] == quiz_id

        assert question[
            "question_type"
        ] == "mcq"

        assert question[
            "difficulty"
        ] == "easy"

        assert "correct_answer" not in question


# EXT-006: Verify negative marking for wrong answers.
def test_ext_006_negative_marking(
    client,
    admin_headers,
    student_headers
):

    category_response = client.post(
        "/api/v1/categories",
        json={
            "name": "EXT-006 Category",
            "description": (
                "Category for testing "
                "negative marking."
            )
        },
        headers=admin_headers
    )

    assert category_response.status_code in [
        200,
        201
    ]

    category_id = category_response.json()[
        "category_id"
    ]


    quiz_response = client.post(
        "/api/v1/quizzes",
        json={
            "title": "EXT-006 Quiz",
            "description": (
                "Quiz for testing "
                "negative marking."
            ),
            "category_id": category_id,
            "duration": 30,
            "total_marks": 100,
            "negative_marks": 5
        },
        headers=admin_headers
    )

    assert quiz_response.status_code in [
        200,
        201
    ]

    quiz_id = quiz_response.json()[
        "quiz_id"
    ]


    for index in range(
        1,
        5
    ):

        question_response = client.post(
            "/api/v1/questions",
            json={
                "quiz_id": quiz_id,
                "question": (
                    f"EXT-006 question "
                    f"number {index}?"
                ),
                "options": [
                    f"Correct {index}",
                    f"Wrong A {index}",
                    f"Wrong B {index}",
                    f"Wrong C {index}"
                ],
                "correct_answer": (
                    f"Correct {index}"
                ),
                "question_type": "mcq",
                "difficulty": "easy"
            },
            headers=admin_headers
        )

        assert question_response.status_code in [
            200,
            201
        ]


    attempt_response = client.post(
        "/api/v1/attempts/start",
        json={
            "quiz_id": quiz_id
        },
        headers=student_headers
    )

    assert attempt_response.status_code in [
        200,
        201
    ]

    attempt_id = attempt_response.json()[
        "attempt_id"
    ]


    resume_response = client.get(
        (
            f"/api/v1/attempts/"
            f"{attempt_id}"
        ),
        headers=student_headers
    )

    assert resume_response.status_code == 200

    questions = resume_response.json()[
        "question_snapshot"
    ]

    assert len(questions) == 4


    first_question = questions[0]

    second_question = questions[1]

    third_question = questions[2]


    answers = {
        first_question["id"]:
            first_question["options"][0],

        second_question["id"]:
            second_question["options"][0],

        third_question["id"]:
            third_question["options"][1]
    }


    submit_response = client.post(
        (
            f"/api/v1/attempts/"
            f"{attempt_id}/submit"
        ),
        json={
            "answers": answers
        },
        headers=student_headers
    )

    assert submit_response.status_code == 200


    results_response = client.get(
        "/api/v1/results/me",
        headers=student_headers
    )

    assert results_response.status_code == 200

    matching_results = [
        result
        for result in results_response.json()
        if result["attempt_id"] == attempt_id
    ]

    assert len(matching_results) == 1

    result = matching_results[0]


    assert result[
        "score_obtained"
    ] == 45.0

    assert result[
        "percentage"
    ] == 45.0

    assert result[
        "status"
    ] == "pass"


    result_id = result[
        "result_id"
    ]


    breakdown_response = client.get(
        (
            f"/api/v1/results/"
            f"{result_id}/breakdown"
        ),
        headers=student_headers
    )

    assert breakdown_response.status_code == 200

    breakdown = breakdown_response.json()


    correct_questions = [
        question
        for question in breakdown
        if question["is_correct"] is True
    ]

    wrong_questions = [
        question
        for question in breakdown
        if (
            question["selected_answer"]
            is not None
            and question["is_correct"] is False
        )
    ]

    unanswered_questions = [
        question
        for question in breakdown
        if question["selected_answer"] is None
    ]


    assert len(correct_questions) == 2

    assert len(wrong_questions) == 1

    assert len(unanswered_questions) == 1


    for question in correct_questions:

        assert question[
            "marks_obtained"
        ] == 25.0


    assert wrong_questions[0][
        "marks_obtained"
    ] == -5.0


    assert unanswered_questions[0][
        "marks_obtained"
    ] == 0.0


    # EXT-007: Verify partial marking for multiple-select questions.
def test_ext_007_partial_marking_multiple_select(
    client,
    admin_headers,
    student_headers
):

    category_response = client.post(
        "/api/v1/categories",
        json={
            "name": "EXT-007 Category",
            "description": (
                "Category for testing "
                "multiple-select partial marking."
            )
        },
        headers=admin_headers
    )

    assert category_response.status_code in [
        200,
        201
    ]

    category_id = category_response.json()[
        "category_id"
    ]


    quiz_response = client.post(
        "/api/v1/quizzes",
        json={
            "title": "EXT-007 Quiz",
            "description": (
                "Quiz for testing partial marking "
                "for multiple-select questions."
            ),
            "category_id": category_id,
            "duration": 30,
            "total_marks": 10,
            "negative_marks": 0
        },
        headers=admin_headers
    )

    assert quiz_response.status_code in [
        200,
        201
    ]

    quiz_id = quiz_response.json()[
        "quiz_id"
    ]


    question_response = client.post(
        "/api/v1/questions",
        json={
            "quiz_id": quiz_id,
            "question": (
                "Which of the following are "
                "programming languages?"
            ),
            "options": [
                "Python",
                "Java",
                "HTML",
                "C++"
            ],
            "correct_answer": [
                "Python",
                "Java",
                "C++"
            ],
            "question_type": (
                "multiple_select"
            ),
            "difficulty": "medium"
        },
        headers=admin_headers
    )

    assert question_response.status_code in [
        200,
        201
    ]


    attempt_response = client.post(
        "/api/v1/attempts/start",
        json={
            "quiz_id": quiz_id
        },
        headers=student_headers
    )

    assert attempt_response.status_code in [
        200,
        201
    ]

    attempt_id = attempt_response.json()[
        "attempt_id"
    ]


    resume_response = client.get(
        (
            f"/api/v1/attempts/"
            f"{attempt_id}"
        ),
        headers=student_headers
    )

    assert resume_response.status_code == 200

    questions = resume_response.json()[
        "question_snapshot"
    ]

    assert len(questions) == 1

    question_id = questions[0][
        "id"
    ]


    submit_response = client.post(
        (
            f"/api/v1/attempts/"
            f"{attempt_id}/submit"
        ),
        json={
            "answers": {
                question_id: [
                    "Python",
                    "Java"
                ]
            }
        },
        headers=student_headers
    )

    assert submit_response.status_code == 200


    results_response = client.get(
        "/api/v1/results/me",
        headers=student_headers
    )

    assert results_response.status_code == 200

    matching_results = [
        result
        for result in results_response.json()
        if result["attempt_id"] == attempt_id
    ]

    assert len(matching_results) == 1

    result = matching_results[0]


    expected_score = round(
        (
            2 / 3
        ) * 10,
        2
    )

    assert round(
        result["score_obtained"],
        2
    ) == expected_score

    assert round(
        result["percentage"],
        2
    ) == 66.67

    assert result[
        "status"
    ] == "pass"


    result_id = result[
        "result_id"
    ]


    breakdown_response = client.get(
        (
            f"/api/v1/results/"
            f"{result_id}/breakdown"
        ),
        headers=student_headers
    )

    assert breakdown_response.status_code == 200

    breakdown = breakdown_response.json()

    assert len(breakdown) == 1

    question_result = breakdown[0]


    assert question_result[
        "selected_answer"
    ] == [
        "Python",
        "Java"
    ]

    assert set(
        question_result[
            "correct_answer"
        ]
    ) == {
        "Python",
        "Java",
        "C++"
    }

    assert question_result[
        "is_correct"
    ] is False

    assert round(
        question_result[
            "marks_obtained"
        ],
        2
    ) == 6.67