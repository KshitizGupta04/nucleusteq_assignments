import random

from datetime import (
    datetime,
    timedelta
)

from app.constants.messages import (
    ErrorMessages
)

from app.exceptions.customexceptions import (
    AttemptAlreadySubmittedException,
    AttemptNotFoundException,
    ForbiddenException,
    InvalidAnswerException,
    MaxAttemptReachedException,
    QuestionNotFoundException,
    AttemptAlreadyInProgressException,
    QuizNotFoundException
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
    AttemptQuestionResponse,
    ResumeAttemptResponse,
    SaveAnswerRequest,
    StartAttemptRequest,
    SubmitAttemptRequest
)

from app.services.result_service import (
    ResultService
)


class AttemptService:

    MAX_ATTEMPTS = 3


    @staticmethod
    def _verify_attempt_owner(
        attempt: dict,
        current_user
    ):

        if (
            attempt["student_id"]
            != current_user["sub"]
        ):

            raise ForbiddenException()


    @staticmethod
    def _get_question_id(
        question: dict
    ) -> str:

        return str(
            question.get(
                "id",
                question.get("_id", "")
            )
        )


    @staticmethod
    def _get_safe_question_snapshot(
        questions: list
    ):

        return [
            AttemptQuestionResponse(
                id=AttemptService._get_question_id(
                    question
                ),
                quiz_id=question[
                    "quiz_id"
                ],
                question=question[
                    "question"
                ],
                options=question[
                    "options"
                ],
                question_type=question[
                    "question_type"
                ],
                difficulty=question[
                    "difficulty"
                ]
            )

            for question in questions
        ]


    @staticmethod
    def _get_expiry_time(
        attempt: dict,
        quiz: dict
    ) -> datetime:

        return (
            attempt["started_at"]
            + timedelta(
                minutes=quiz["duration"]
            )
        )


    @staticmethod
    def _calculate_score(
        attempt: dict,
        answers: dict,
        quiz: dict
    ) -> float:

        total_questions = len(
            attempt[
                "question_snapshot"
            ]
        )

        total_marks = float(
            quiz["total_marks"]
        )

        marks_per_question = (
            total_marks / total_questions
            if total_questions > 0
            else 0.0
        )

        score = 0.0

        for question in attempt[
            "question_snapshot"
        ]:

            question_id = (
                AttemptService._get_question_id(
                    question
                )
            )

            student_answer = (
                answers.get(
                    question_id
                )
            )

            if (
                student_answer is not None
                and student_answer ==
                question["correct_answer"]
            ):

                score += marks_per_question

        return score


    @staticmethod
    def _complete_attempt(
        attempt_id: str,
        attempt: dict,
        answers: dict,
        quiz: dict
    ):

        score = (
            AttemptService._calculate_score(
                attempt,
                answers,
                quiz
            )
        )

        AttemptRepository.update_attempt(
            attempt_id,
            {
                "answers": answers,
                "score": score,
                "status": "submitted",
                "submitted_at": datetime.utcnow()
            }
        )

        ResultService.generate_result(
            attempt_id
        )


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


        active_attempt = (
            AttemptRepository
            .get_latest_in_progress_attempt(
                student_id,
                request.quiz_id
            )
        )

        if active_attempt:

            expires_at = (
                AttemptService._get_expiry_time(
                    active_attempt,
                    quiz
                )
            )

            if (
                datetime.utcnow() >=
                expires_at
            ):

                attempt_id = str(
                    active_attempt["_id"]
                )

                saved_answers = (
                    active_attempt.get(
                        "answers",
                        {}
                    )
                )

                AttemptService._complete_attempt(
                    attempt_id,
                    active_attempt,
                    saved_answers,
                    quiz
                )

            else:

                raise (
                    AttemptAlreadyInProgressException()
                )


        attempt_count = (
            AttemptRepository.count_attempts(
                student_id,
                request.quiz_id
            )
        )


        if (
            attempt_count >=
            AttemptService.MAX_ATTEMPTS
        ):

            raise MaxAttemptReachedException()


        questions = (
            QuestionRepository
            .get_questions_by_quiz_id(
                request.quiz_id
            )
        )


        snapshot = [
            question.copy()
            for question in questions
        ]


        random.shuffle(
            snapshot
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


        expires_at = (
            attempt.started_at
            + timedelta(
                minutes=quiz["duration"]
            )
        )


        return AttemptCreateResponse(
            message=ErrorMessages.ATTEMPT_STARTED,
            attempt_id=attempt_id,
            resumed=False,
            started_at=attempt.started_at,
            expires_at=expires_at
        )


    @staticmethod
    def save_answer(
        attempt_id: str,
        request: SaveAnswerRequest,
        current_user
    ):

        attempt = (
            AttemptRepository.get_attempt_by_id(
                attempt_id
            )
        )


        if not attempt:

            raise AttemptNotFoundException()


        AttemptService._verify_attempt_owner(
            attempt,
            current_user
        )


        if (
            attempt["status"] ==
            "submitted"
        ):

            raise AttemptAlreadySubmittedException()


        quiz = (
            QuizRepository.get_quiz_by_id(
                attempt["quiz_id"]
            )
        )


        if not quiz:

            raise QuizNotFoundException()


        expires_at = (
            AttemptService._get_expiry_time(
                attempt,
                quiz
            )
        )


        if (
            datetime.utcnow() >=
            expires_at
        ):

            saved_answers = (
                attempt.get(
                    "answers",
                    {}
                )
            )

            AttemptService._complete_attempt(
                attempt_id,
                attempt,
                saved_answers,
                quiz
            )

            raise AttemptAlreadySubmittedException()


        selected_question = None


        for question in attempt[
            "question_snapshot"
        ]:

            question_id = (
                AttemptService._get_question_id(
                    question
                )
            )

            if (
                question_id ==
                request.question_id
            ):

                selected_question = question

                break


        if not selected_question:

            raise QuestionNotFoundException()


        if (
            request.answer not in
            selected_question["options"]
        ):

            raise InvalidAnswerException()


        AttemptRepository.save_answer(
            attempt_id,
            request.question_id,
            request.answer
        )


        return AttemptMessageResponse(
            message=ErrorMessages.ANSWER_SAVED
        )


    @staticmethod
    def resume_attempt(
        attempt_id: str,
        current_user
    ):

        attempt = (
            AttemptRepository.get_attempt_by_id(
                attempt_id
            )
        )


        if not attempt:

            raise AttemptNotFoundException()


        AttemptService._verify_attempt_owner(
            attempt,
            current_user
        )


        quiz = (
            QuizRepository.get_quiz_by_id(
                attempt["quiz_id"]
            )
        )


        if not quiz:

            raise QuizNotFoundException()


        expires_at = (
            AttemptService._get_expiry_time(
                attempt,
                quiz
            )
        )


        if (
            attempt["status"] ==
            "in_progress"
            and datetime.utcnow() >=
            expires_at
        ):

            saved_answers = (
                attempt.get(
                    "answers",
                    {}
                )
            )

            AttemptService._complete_attempt(
                attempt_id,
                attempt,
                saved_answers,
                quiz
            )

            attempt = (
                AttemptRepository
                .get_attempt_by_id(
                    attempt_id
                )
            )


        safe_questions = (
            AttemptService
            ._get_safe_question_snapshot(
                attempt[
                    "question_snapshot"
                ]
            )
        )


        return ResumeAttemptResponse(
            attempt_id=str(
                attempt["_id"]
            ),
            quiz_id=attempt[
                "quiz_id"
            ],
            question_snapshot=safe_questions,
            answers=attempt.get(
                "answers",
                {}
            ),
            status=attempt[
                "status"
            ],
            started_at=attempt[
                "started_at"
            ],
            expires_at=expires_at
        )


    @staticmethod
    def submit_attempt(
        attempt_id: str,
        request: SubmitAttemptRequest,
        current_user
    ):

        attempt = (
            AttemptRepository.get_attempt_by_id(
                attempt_id
            )
        )


        if not attempt:

            raise AttemptNotFoundException()


        AttemptService._verify_attempt_owner(
            attempt,
            current_user
        )


        if (
            attempt["status"] ==
            "submitted"
        ):

            raise AttemptAlreadySubmittedException()


        question_map = {
            AttemptService._get_question_id(
                question
            ): question

            for question in attempt[
                "question_snapshot"
            ]
        }


        for (
            question_id,
            answer
        ) in request.answers.items():

            question = question_map.get(
                question_id
            )

            if not question:

                raise QuestionNotFoundException()

            if (
                answer not in
                question["options"]
            ):

                raise InvalidAnswerException()


        quiz = (
            QuizRepository.get_quiz_by_id(
                attempt["quiz_id"]
            )
        )


        if not quiz:

            raise QuizNotFoundException()


        AttemptService._complete_attempt(
            attempt_id,
            attempt,
            request.answers,
            quiz
        )


        return AttemptMessageResponse(
            message=ErrorMessages.ATTEMPT_SUBMITTED
        )