from datetime import (
    datetime
)

from app.constants.messages import (
    ErrorMessages
)

from app.exceptions.customexceptions import (
    AttemptAlreadySubmittedException,
    AttemptNotFoundException,
    MaxAttemptReachedException,
    QuizNotFoundException,
    InvalidAnswerException,
    QuestionNotFoundException,
    AttemptAlreadyInProgressException
)

from app.models.attempt import (
    Attempt
)

from app.repositories.attempt_repository import (
    AttemptRepository
)

from app.repositories.question_repository import (
    QuestionRepository
)

from app.repositories.quiz_repository import (
    QuizRepository
)

from app.schemas.attempt_schema import (
    AttemptCreateResponse,
    AttemptMessageResponse,
    ResumeAttemptResponse,
    SaveAnswerRequest,
    StartAttemptRequest,
    SubmitAttemptRequest
)

from app.services.result_service import (
    ResultService
)


class AttemptService:

    @staticmethod
    def start_attempt(
        request: StartAttemptRequest,
        current_user
    ):

        student_id = current_user["sub"]

        quiz = (
            QuizRepository.get_quiz_by_id(
                request.quiz_id
            )
        )

        if not quiz:

            raise QuizNotFoundException()

        attempt_count = (
            AttemptRepository.count_attempts(
                student_id,
                request.quiz_id
            )
        )

        if attempt_count >= 3:

            raise MaxAttemptReachedException()

        active_attempt = (
            AttemptRepository.get_in_progress_attempt(
                student_id,
                request.quiz_id
            )
        )

        if active_attempt:

            raise AttemptAlreadyInProgressException()

        questions = (
            QuestionRepository.get_questions_by_quiz_id(
                request.quiz_id
            )
        )

        snapshot = []

        for question in questions:

            snapshot.append(
                question
            )

        attempt = Attempt(
            quiz_id=request.quiz_id,
            student_id=student_id,
            attempt_number=attempt_count + 1,
            question_snapshot=snapshot
        )

        attempt_id = (
            AttemptRepository.create_attempt(
                attempt.model_dump()
            )
        )

        response = AttemptCreateResponse(
            message=ErrorMessages.ATTEMPT_STARTED,
            attempt_id=attempt_id
        )

        return response

    @staticmethod
    def save_answer(
        attempt_id: str,
        request: SaveAnswerRequest
    ):

        attempt = (
            AttemptRepository.get_attempt_by_id(
                attempt_id
            )
        )

        if not attempt:

            raise AttemptNotFoundException()

        if attempt["status"] == "submitted":

            raise AttemptAlreadySubmittedException()

        selected_question = None

        for question in attempt[
            "question_snapshot"
        ]:

            if str(
                question["_id"]
            ) == request.question_id:

                selected_question = question

                break

        if not selected_question:

            raise QuestionNotFoundException()

        if request.answer not in selected_question[
            "options"
        ]:

            raise InvalidAnswerException()

        AttemptRepository.save_answer(
            attempt_id,
            request.question_id,
            request.answer
        )

        response = AttemptMessageResponse(
            message=ErrorMessages.ANSWER_SAVED
        )

        return response

    @staticmethod
    def resume_attempt(
        attempt_id: str
    ):

        attempt = (
            AttemptRepository.get_attempt_by_id(
                attempt_id
            )
        )

        if not attempt:

            raise AttemptNotFoundException()

        response = ResumeAttemptResponse(
            attempt_id=str(
                attempt["_id"]
            ),
            quiz_id=attempt[
                "quiz_id"
            ],
            question_snapshot=attempt[
                "question_snapshot"
            ],
            answers=attempt[
                "answers"
            ],
            status=attempt[
                "status"
            ]
        )

        return response

    @staticmethod
    def submit_attempt(
        attempt_id: str,
        request: SubmitAttemptRequest
    ):

        attempt = (
            AttemptRepository.get_attempt_by_id(
                attempt_id
            )
        )

        if not attempt:

            raise AttemptNotFoundException()

        if attempt["status"] == "submitted":

            raise AttemptAlreadySubmittedException()

        score = 0

        total_questions = len(
            attempt[
                "question_snapshot"
            ]
        )

        if total_questions > 0:

            quiz = (
                QuizRepository.get_quiz_by_id(
                    attempt[
                        "quiz_id"
                    ]
                )
            )

            marks_per_question = (
                quiz["total_marks"] /
                total_questions
            )

        else:

            marks_per_question = 0

        for question in attempt[
            "question_snapshot"
        ]:

            question_id = str(
                question["_id"]
            )

            correct_answer = question[
                "correct_answer"
            ]

            student_answer = (
                request.answers.get(
                    question_id
                )
            )

            if (
                student_answer
                and student_answer ==
                correct_answer
            ):

                score += marks_per_question

        AttemptRepository.update_attempt(
            attempt_id,
            {
                "answers": request.answers,
                "score": score,
                "status": "submitted",
                "submitted_at": datetime.utcnow()
            }
        )

        ResultService.generate_result(
            attempt_id
        )

        response = AttemptMessageResponse(
            message=ErrorMessages.ATTEMPT_SUBMITTED
        )

        return response