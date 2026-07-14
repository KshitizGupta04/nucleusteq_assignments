import uuid

from datetime import (
    datetime,
    timedelta
)

from app.repositories.attempt_repository import (
    AttemptRepository
)


CATEGORY_URL = "/api/v1/categories"

QUIZ_URL = "/api/v1/quizzes"

QUESTION_URL = "/api/v1/questions"

ATTEMPT_URL = "/api/v1/attempts"


def create_category(
    client,
    admin_headers
):

    unique = uuid.uuid4().hex[:8]

    response = client.post(
        CATEGORY_URL + "/",
        json={
            "name": (
                f"Attempt_Category_{unique}"
            ),
            "description": (
                "Category for attempt testing"
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
    category_id,
    duration=30
):

    unique = uuid.uuid4().hex[:8]

    response = client.post(
        QUIZ_URL + "/",
        json={
            "title": (
                f"Attempt_Quiz_{unique}"
            ),
            "description": (
                "Quiz for attempt testing"
            ),
            "category_id": category_id,
            "duration": duration,
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
    quiz_id
):

    response = client.post(
        QUESTION_URL + "/",
        json={
            "quiz_id": quiz_id,
            "question": (
                "Which language is platform independent?"
            ),
            "options": [
                "Java",
                "C",
                "HTML",
                "CSS"
            ],
            "correct_answer": "Java",
            "question_type": "mcq",
            "difficulty": "easy"
        },
        headers=admin_headers
    )

    assert response.status_code == 200

    return response.json()[
        "question_id"
    ]


def setup_quiz_with_question(
    client,
    admin_headers,
    duration=30
):

    category_id = create_category(
        client,
        admin_headers
    )

    quiz_id = create_quiz(
        client,
        admin_headers,
        category_id,
        duration
    )

    question_id = create_question(
        client,
        admin_headers,
        quiz_id
    )

    return (
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

    return response


# SRS QUIZ ATTEMPT SERVICE TEST CASES


# ATT-001: Start Quiz Attempt


def test_att_001_start_quiz_attempt(
    client,
    admin_headers,
    student_headers
):

    quiz_id, _ = setup_quiz_with_question(
        client,
        admin_headers
    )

    response = client.post(
        ATTEMPT_URL + "/start",
        json={
            "quiz_id": quiz_id
        },
        headers=student_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert "attempt_id" in data

    assert (
        data["message"]
        == "Attempt started successfully."
    )


# ATT-002: Create Question Snapshot


def test_att_002_create_question_snapshot(
    client,
    admin_headers,
    student_headers
):

    quiz_id, question_id = (
        setup_quiz_with_question(
            client,
            admin_headers
        )
    )

    start_response = start_attempt(
        client,
        student_headers,
        quiz_id
    )

    attempt_id = start_response.json()[
        "attempt_id"
    ]

    response = client.get(
        f"{ATTEMPT_URL}/{attempt_id}",
        headers=student_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert "question_snapshot" in data

    assert isinstance(
        data["question_snapshot"],
        list
    )

    assert len(
        data["question_snapshot"]
    ) == 1

    snapshot = data[
        "question_snapshot"
    ][0]

    assert (
        snapshot["id"]
        == question_id
    )

    assert (
        snapshot["quiz_id"]
        == quiz_id
    )

    assert (
        snapshot["question"]
        == (
            "Which language is "
            "platform independent?"
        )
    )

    assert snapshot["options"] == [
        "Java",
        "C",
        "HTML",
        "CSS"
    ]

    assert "correct_answer" not in snapshot


# ATT-003: Save Partial Answers


def test_att_003_save_partial_answers(
    client,
    admin_headers,
    student_headers
):

    quiz_id, question_id = (
        setup_quiz_with_question(
            client,
            admin_headers
        )
    )

    start_response = start_attempt(
        client,
        student_headers,
        quiz_id
    )

    attempt_id = start_response.json()[
        "attempt_id"
    ]

    response = client.put(
        (
            f"{ATTEMPT_URL}/"
            f"{attempt_id}/answer"
        ),
        json={
            "question_id": question_id,
            "answer": "Java"
        },
        headers=student_headers
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        == "Answer saved successfully."
    )


# ATT-004: Resume Attempt


def test_att_004_resume_attempt(
    client,
    admin_headers,
    student_headers
):

    quiz_id, question_id = (
        setup_quiz_with_question(
            client,
            admin_headers
        )
    )

    start_response = start_attempt(
        client,
        student_headers,
        quiz_id
    )

    attempt_id = start_response.json()[
        "attempt_id"
    ]

    save_response = client.put(
        (
            f"{ATTEMPT_URL}/"
            f"{attempt_id}/answer"
        ),
        json={
            "question_id": question_id,
            "answer": "Java"
        },
        headers=student_headers
    )

    assert save_response.status_code == 200

    response = client.get(
        f"{ATTEMPT_URL}/{attempt_id}",
        headers=student_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert "answers" in data

    assert (
        data["answers"][question_id]
        == "Java"
    )


# ATT-005: Submit Quiz


def test_att_005_submit_quiz(
    client,
    admin_headers,
    student_headers
):

    quiz_id, question_id = (
        setup_quiz_with_question(
            client,
            admin_headers
        )
    )

    start_response = start_attempt(
        client,
        student_headers,
        quiz_id
    )

    attempt_id = start_response.json()[
        "attempt_id"
    ]

    response = client.post(
        (
            f"{ATTEMPT_URL}/"
            f"{attempt_id}/submit"
        ),
        json={
            "answers": {
                question_id: "Java"
            }
        },
        headers=student_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["message"]
        == "Attempt submitted successfully."
    )


# ATT-006: Submit After Time Expiry


def test_att_006_submit_after_time_expiry(
    client,
    admin_headers,
    student_headers
):

    quiz_id, question_id = (
        setup_quiz_with_question(
            client,
            admin_headers,
            duration=1
        )
    )

    start_response = start_attempt(
        client,
        student_headers,
        quiz_id
    )

    attempt_id = start_response.json()[
        "attempt_id"
    ]

    expired_started_at = (
        datetime.utcnow()
        - timedelta(
            minutes=2
        )
    )

    update_result = (
        AttemptRepository.update_attempt(
            attempt_id,
            {
                "started_at": (
                    expired_started_at
                )
            }
        )
    )

    assert update_result is not None

    response = client.post(
        (
            f"{ATTEMPT_URL}/"
            f"{attempt_id}/submit"
        ),
        json={
            "answers": {
                question_id: "Java"
            }
        },
        headers=student_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["message"]
        == "Attempt submitted successfully."
    )

    stored_attempt = (
        AttemptRepository.get_attempt_by_id(
            attempt_id
        )
    )

    assert stored_attempt is not None

    assert (
        stored_attempt["status"]
        == "submitted"
    )


# ATT-007: Re-attempt Quiz
# Max Attempts Reached


def test_att_007_reattempt_quiz_max_limit(
    client,
    admin_headers,
    student_headers
):

    quiz_id, question_id = (
        setup_quiz_with_question(
            client,
            admin_headers
        )
    )

    for _ in range(3):

        start_response = start_attempt(
            client,
            student_headers,
            quiz_id
        )

        attempt_id = (
            start_response.json()[
                "attempt_id"
            ]
        )

        submit_response = client.post(
            (
                f"{ATTEMPT_URL}/"
                f"{attempt_id}/submit"
            ),
            json={
                "answers": {
                    question_id: "Java"
                }
            },
            headers=student_headers
        )

        assert (
            submit_response.status_code
            == 200
        )

    response = client.post(
        ATTEMPT_URL + "/start",
        json={
            "quiz_id": quiz_id
        },
        headers=student_headers
    )

    assert response.status_code == 400


# ATT-008: Attempt Invalid Quiz


def test_att_008_attempt_invalid_quiz(
    client,
    student_headers
):

    response = client.post(
        ATTEMPT_URL + "/start",
        json={
            "quiz_id": (
                "689999999999999999999999"
            )
        },
        headers=student_headers
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Quiz not found."
    )


# ADDITIONAL ATTEMPT TEST CASES


# ADDITIONAL: Attempt Without Token


def test_attempt_without_token(
    client
):

    response = client.post(
        ATTEMPT_URL + "/start",
        json={
            "quiz_id": (
                "689999999999999999999999"
            )
        }
    )

    assert response.status_code == 401


# ADDITIONAL: Admin Cannot Start Attempt


def test_admin_cannot_start_attempt(
    client,
    admin_headers
):

    response = client.post(
        ATTEMPT_URL + "/start",
        json={
            "quiz_id": (
                "689999999999999999999999"
            )
        },
        headers=admin_headers
    )

    assert response.status_code == 403


# ADDITIONAL: Invalid Answer


def test_invalid_answer(
    client,
    admin_headers,
    student_headers
):

    quiz_id, question_id = (
        setup_quiz_with_question(
            client,
            admin_headers
        )
    )

    start_response = start_attempt(
        client,
        student_headers,
        quiz_id
    )

    attempt_id = start_response.json()[
        "attempt_id"
    ]

    response = client.put(
        (
            f"{ATTEMPT_URL}/"
            f"{attempt_id}/answer"
        ),
        json={
            "question_id": question_id,
            "answer": "Invalid Answer"
        },
        headers=student_headers
    )

    assert response.status_code == 400


# ADDITIONAL: Attempt Already Submitted


def test_attempt_already_submitted(
    client,
    admin_headers,
    student_headers
):

    quiz_id, question_id = (
        setup_quiz_with_question(
            client,
            admin_headers
        )
    )

    start_response = start_attempt(
        client,
        student_headers,
        quiz_id
    )

    attempt_id = start_response.json()[
        "attempt_id"
    ]

    first_response = client.post(
        (
            f"{ATTEMPT_URL}/"
            f"{attempt_id}/submit"
        ),
        json={
            "answers": {
                question_id: "Java"
            }
        },
        headers=student_headers
    )

    assert first_response.status_code == 200

    second_response = client.post(
        (
            f"{ATTEMPT_URL}/"
            f"{attempt_id}/submit"
        ),
        json={
            "answers": {
                question_id: "Java"
            }
        },
        headers=student_headers
    )

    assert second_response.status_code == 400


# ADDITIONAL: Attempt Already In Progress
def test_attempt_already_in_progress(
    client,
    admin_headers,
    student_headers
):

    quiz_id, _ = setup_quiz_with_question(
        client,
        admin_headers
    )

    first_response = client.post(
        ATTEMPT_URL + "/start",
        json={
            "quiz_id": quiz_id
        },
        headers=student_headers
    )

    assert first_response.status_code == 200

    first_attempt_id = (
        first_response.json()[
            "attempt_id"
        ]
    )

    response = client.post(
        ATTEMPT_URL + "/start",
        json={
            "quiz_id": quiz_id
        },
        headers=student_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["attempt_id"]
        == first_attempt_id
    )

    assert data["resumed"] is True

    assert (
        data["message"]
        == (
            "Active attempt resumed successfully."
        )
    )



# EXT-001
# Randomize Question Order Per Attempt
# Expected Result:
# Questions are randomized when an attempt
# starts and the same randomized order is
# preserved when the attempt is resumed.


def test_ext_001_randomize_question_order_per_attempt(
    client,
    admin_headers,
    student_headers,
    monkeypatch
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

    question_ids = []

    questions_data = [
        {
            "question": (
                "Which keyword is used "
                "to define a class in Java?"
            ),
            "options": [
                "class",
                "define",
                "object",
                "new"
            ],
            "correct_answer": "class"
        },
        {
            "question": (
                "Which keyword is used "
                "to create an object in Java?"
            ),
            "options": [
                "new",
                "create",
                "object",
                "make"
            ],
            "correct_answer": "new"
        },
        {
            "question": (
                "Which method is the entry "
                "point of a Java program?"
            ),
            "options": [
                "main",
                "start",
                "run",
                "execute"
            ],
            "correct_answer": "main"
        }
    ]

    for question_data in questions_data:

        response = client.post(
            QUESTION_URL + "/",
            headers=admin_headers,
            json={
                "quiz_id": quiz_id,
                "question": question_data[
                    "question"
                ],
                "options": question_data[
                    "options"
                ],
                "correct_answer": (
                    question_data[
                        "correct_answer"
                    ]
                ),
                "question_type": "mcq",
                "difficulty": "easy"
            }
        )

        assert response.status_code == 200

        question_ids.append(
            response.json()[
                "question_id"
            ]
        )

    def reverse_questions(
        snapshot
    ):

        snapshot.reverse()

    monkeypatch.setattr(
        "app.services.attempt_service."
        "random.shuffle",
        reverse_questions
    )

    start_response = client.post(
        ATTEMPT_URL + "/start",
        headers=student_headers,
        json={
            "quiz_id": quiz_id
        }
    )

    assert start_response.status_code == 200

    attempt_id = start_response.json()[
        "attempt_id"
    ]

    attempt = (
        AttemptRepository.get_attempt_by_id(
            attempt_id
        )
    )

    assert attempt is not None

    stored_order = [
        str(
            question.get(
                "id",
                question.get(
                    "_id",
                    ""
                )
            )
        )
        for question in attempt[
            "question_snapshot"
        ]
    ]

    assert stored_order == list(
        reversed(
            question_ids
        )
    )

    resume_response = client.get(
        f"{ATTEMPT_URL}/{attempt_id}",
        headers=student_headers
    )

    assert resume_response.status_code == 200

    resumed_order = [
        question["id"]
        for question in resume_response.json()[
            "question_snapshot"
        ]
    ]

    assert resumed_order == stored_order


# EXT-008:
# Verify quiz scheduling and availability-window restrictions.
def test_ext_008_quiz_scheduling(
    client,
    admin_headers,
    student_headers
):

    from datetime import (
        datetime,
        timedelta
    )


    # Create a category for EXT-008 quizzes.
    category_response = client.post(
        "/api/v1/categories",
        json={
            "name": "EXT-008 Category",
            "description": (
                "Category for testing "
                "quiz scheduling."
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


    current_time = datetime.now()


    # CASE 1:
    # Quiz availability has not started yet.
    future_quiz_response = client.post(
        "/api/v1/quizzes",
        json={
            "title": "EXT-008 Future Quiz",
            "description": (
                "Quiz that is not yet available."
            ),
            "category_id": category_id,
            "duration": 30,
            "total_marks": 10,
            "available_from": (
                current_time
                + timedelta(hours=1)
            ).isoformat(),
            "available_until": (
                current_time
                + timedelta(hours=2)
            ).isoformat()
        },
        headers=admin_headers
    )

    assert future_quiz_response.status_code in [
        200,
        201
    ]

    future_quiz_id = (
        future_quiz_response.json()[
            "quiz_id"
        ]
    )


    future_attempt_response = client.post(
        "/api/v1/attempts/start",
        json={
            "quiz_id": future_quiz_id
        },
        headers=student_headers
    )

    assert (
        future_attempt_response.status_code
        == 403
    )

    assert future_attempt_response.json()[
        "detail"
    ] == "Quiz is not available yet."


    
    # CASE 2:
    # Quiz availability period has ended.
    expired_quiz_response = client.post(
        "/api/v1/quizzes",
        json={
            "title": "EXT-008 Expired Quiz",
            "description": (
                "Quiz whose availability "
                "period has ended."
            ),
            "category_id": category_id,
            "duration": 30,
            "total_marks": 10,
            "available_from": (
                current_time
                - timedelta(hours=2)
            ).isoformat(),
            "available_until": (
                current_time
                - timedelta(hours=1)
            ).isoformat()
        },
        headers=admin_headers
    )

    assert expired_quiz_response.status_code in [
        200,
        201
    ]

    expired_quiz_id = (
        expired_quiz_response.json()[
            "quiz_id"
        ]
    )


    expired_attempt_response = client.post(
        "/api/v1/attempts/start",
        json={
            "quiz_id": expired_quiz_id
        },
        headers=student_headers
    )

    assert (
        expired_attempt_response.status_code
        == 403
    )

    assert expired_attempt_response.json()[
        "detail"
    ] == (
        "Quiz availability period has ended."
    )


    # CASE 3:
    # Current time is inside availability window.
    active_quiz_response = client.post(
        "/api/v1/quizzes",
        json={
            "title": "EXT-008 Active Quiz",
            "description": (
                "Quiz that is currently available."
            ),
            "category_id": category_id,
            "duration": 30,
            "total_marks": 10,
            "available_from": (
                current_time
                - timedelta(hours=1)
            ).isoformat(),
            "available_until": (
                current_time
                + timedelta(hours=1)
            ).isoformat()
        },
        headers=admin_headers
    )

    assert active_quiz_response.status_code in [
        200,
        201
    ]

    active_quiz_id = (
        active_quiz_response.json()[
            "quiz_id"
        ]
    )


    active_attempt_response = client.post(
        "/api/v1/attempts/start",
        json={
            "quiz_id": active_quiz_id
        },
        headers=student_headers
    )

    assert active_attempt_response.status_code in [
        200,
        201
    ]

    assert (
        active_attempt_response.json()[
            "attempt_id"
        ]
    )