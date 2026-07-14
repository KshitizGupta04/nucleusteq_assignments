import random

from datetime import (
    datetime,
    timedelta
)

from app.constants.messages import (
    ErrorMessages
)

from app.core.logger import (
    logger
)

from app.exceptions.customexceptions import (
    AttemptAlreadySubmittedException,
    AttemptNotFoundException,
    ForbiddenException,
    InvalidAnswerException,
    MaxAttemptReachedException,
    QuestionNotFoundException,
    QuizExpiredException,
    QuizNotFoundException,
    QuizNotStartedException
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

            logger.warning(
                "Attempt access denied: "
                "student='%s' tried to access "
                "an attempt owned by student='%s'.",
                current_user["sub"],
                attempt["student_id"]
            )

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
    def _validate_quiz_availability(
        quiz: dict
    ):

        current_time = datetime.now()

        available_from = quiz.get(
            "available_from"
        )

        available_until = quiz.get(
            "available_until"
        )


        if (
            available_from is not None
            and current_time < available_from
        ):

            logger.warning(
                "Quiz attempt blocked: "
                "quiz_id='%s' is not available yet.",
                str(
                    quiz.get(
                        "_id",
                        ""
                    )
                )
            )

            raise QuizNotStartedException()


        if (
            available_until is not None
            and current_time > available_until
        ):

            logger.warning(
                "Quiz attempt blocked: "
                "quiz_id='%s' availability "
                "period has ended.",
                str(
                    quiz.get(
                        "_id",
                        ""
                    )
                )
            )

            raise QuizExpiredException()


    @staticmethod
    def _calculate_multiple_select_score(
        student_answer: list,
        correct_answer: list,
        marks_per_question: float
    ) -> float:

        selected_answers = set(
            student_answer
        )

        correct_answers = set(
            correct_answer
        )

        correct_selections = len(
            selected_answers
            & correct_answers
        )

        incorrect_selections = len(
            selected_answers
            - correct_answers
        )

        partial_ratio = (
            (
                correct_selections
                - incorrect_selections
            )
            / len(correct_answers)
            if correct_answers
            else 0.0
        )

        partial_ratio = max(
            partial_ratio,
            0.0
        )

        return (
            marks_per_question
            * partial_ratio
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

        negative_marks = float(
            quiz.get(
                "negative_marks",
                0.0
            )
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


            if student_answer is None:

                continue


            question_type = question.get(
                "question_type"
            )


            if (
                question_type
                == "multiple_select"
            ):

                partial_score = (
                    AttemptService
                    ._calculate_multiple_select_score(
                        student_answer,
                        question[
                            "correct_answer"
                        ],
                        marks_per_question
                    )
                )

                score += partial_score

                continue


            if (
                question_type
                == "short_answer"
            ):

                is_correct = (
                    student_answer
                    .strip()
                    .casefold()
                    ==
                    question[
                        "correct_answer"
                    ]
                    .strip()
                    .casefold()
                )

            else:

                is_correct = (
                    student_answer ==
                    question["correct_answer"]
                )


            if is_correct:

                score += marks_per_question

            else:

                score -= negative_marks


        return max(
            score,
            0.0
        )


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


        logger.info(
            "Attempt completed successfully: "
            "attempt_id='%s', quiz_id='%s', "
            "student_id='%s', score='%s'.",
            attempt_id,
            attempt["quiz_id"],
            attempt["student_id"],
            score
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

            logger.warning(
                "Attempt start failed: "
                "quiz_id='%s' not found.",
                request.quiz_id
            )

            raise QuizNotFoundException()


        AttemptService._validate_quiz_availability(
            quiz
        )


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
                datetime.utcnow()
                >= expires_at
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


                logger.info(
                    "Expired active attempt "
                    "auto-submitted: "
                    "attempt_id='%s', "
                    "student_id='%s'.",
                    attempt_id,
                    student_id
                )


            else:

                attempt_id = str(
                    active_attempt["_id"]
                )


                logger.info(
                    "Existing active attempt returned: "
                    "attempt_id='%s', "
                    "student_id='%s', "
                    "quiz_id='%s'.",
                    attempt_id,
                    student_id,
                    request.quiz_id
                )


                return AttemptCreateResponse(
                    message=(
                        "Active attempt resumed successfully."
                    ),
                    attempt_id=attempt_id,
                    resumed=True,
                    started_at=active_attempt[
                        "started_at"
                    ],
                    expires_at=expires_at
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

            logger.warning(
                "Attempt start failed: "
                "student_id='%s' reached maximum "
                "attempts for quiz_id='%s'.",
                student_id,
                request.quiz_id
            )

            raise MaxAttemptReachedException()


        questions = (
            QuestionRepository
            .get_questions_by_quiz_id(
                request.quiz_id
            )
        )


        question_count = quiz.get(
            "question_count"
        )


        if (
            question_count is not None
            and question_count < len(
                questions
            )
        ):

            snapshot = random.sample(
                questions,
                question_count
            )

            snapshot = [
                question.copy()
                for question in snapshot
            ]

        else:

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


        logger.info(
            "Attempt started successfully: "
            "attempt_id='%s', quiz_id='%s', "
            "student_id='%s', attempt_number='%s'.",
            attempt_id,
            request.quiz_id,
            student_id,
            attempt_count + 1
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

            logger.warning(
                "Answer save failed: "
                "attempt_id='%s' not found.",
                attempt_id
            )

            raise AttemptNotFoundException()


        AttemptService._verify_attempt_owner(
            attempt,
            current_user
        )


        if (
            attempt["status"]
            == "submitted"
        ):

            logger.warning(
                "Answer save failed: "
                "attempt_id='%s' is already submitted.",
                attempt_id
            )

            raise AttemptAlreadySubmittedException()


        quiz = (
            QuizRepository.get_quiz_by_id(
                attempt["quiz_id"]
            )
        )


        if not quiz:

            logger.warning(
                "Answer save failed: "
                "quiz_id='%s' not found.",
                attempt["quiz_id"]
            )

            raise QuizNotFoundException()


        expires_at = (
            AttemptService._get_expiry_time(
                attempt,
                quiz
            )
        )


        if (
            datetime.utcnow()
            >= expires_at
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


            logger.info(
                "Expired attempt auto-submitted "
                "during answer save: "
                "attempt_id='%s'.",
                attempt_id
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
                question_id
                == request.question_id
            ):

                selected_question = question

                break


        if not selected_question:

            logger.warning(
                "Answer save failed: "
                "question_id='%s' not found "
                "in attempt_id='%s'.",
                request.question_id,
                attempt_id
            )

            raise QuestionNotFoundException()


        question_type = (
            selected_question.get(
                "question_type"
            )
        )


        if (
            question_type
            == "multiple_select"
        ):

            if (
                not isinstance(
                    request.answer,
                    list
                )
                or not request.answer
                or len(
                    set(request.answer)
                ) != len(request.answer)
                or any(
                    answer not in
                    selected_question["options"]
                    for answer in request.answer
                )
            ):

                logger.warning(
                    "Invalid multiple-select answer: "
                    "attempt_id='%s', "
                    "question_id='%s'.",
                    attempt_id,
                    request.question_id
                )

                raise InvalidAnswerException()


        elif (
            question_type
            == "short_answer"
        ):

            if (
                not isinstance(
                    request.answer,
                    str
                )
                or not request.answer.strip()
            ):

                logger.warning(
                    "Invalid short answer: "
                    "attempt_id='%s', "
                    "question_id='%s'.",
                    attempt_id,
                    request.question_id
                )

                raise InvalidAnswerException()


        else:

            if (
                not isinstance(
                    request.answer,
                    str
                )
                or request.answer not in
                selected_question["options"]
            ):

                logger.warning(
                    "Invalid answer: "
                    "attempt_id='%s', "
                    "question_id='%s'.",
                    attempt_id,
                    request.question_id
                )

                raise InvalidAnswerException()


        AttemptRepository.save_answer(
            attempt_id,
            request.question_id,
            request.answer
        )


        logger.info(
            "Answer saved successfully: "
            "attempt_id='%s', question_id='%s'.",
            attempt_id,
            request.question_id
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

            logger.warning(
                "Attempt resume failed: "
                "attempt_id='%s' not found.",
                attempt_id
            )

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

            logger.warning(
                "Attempt resume failed: "
                "quiz_id='%s' not found.",
                attempt["quiz_id"]
            )

            raise QuizNotFoundException()


        expires_at = (
            AttemptService._get_expiry_time(
                attempt,
                quiz
            )
        )


        if (
            attempt["status"]
            == "in_progress"
            and datetime.utcnow()
            >= expires_at
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


            logger.info(
                "Expired attempt auto-submitted "
                "during resume: "
                "attempt_id='%s'.",
                attempt_id
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


        logger.info(
            "Attempt resumed successfully: "
            "attempt_id='%s', student_id='%s', "
            "status='%s'.",
            attempt_id,
            current_user["sub"],
            attempt["status"]
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

            logger.warning(
                "Attempt submission failed: "
                "attempt_id='%s' not found.",
                attempt_id
            )

            raise AttemptNotFoundException()


        AttemptService._verify_attempt_owner(
            attempt,
            current_user
        )


        if (
            attempt["status"]
            == "submitted"
        ):

            logger.warning(
                "Attempt submission failed: "
                "attempt_id='%s' is already submitted.",
                attempt_id
            )

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

                logger.warning(
                    "Attempt submission failed: "
                    "question_id='%s' not found "
                    "in attempt_id='%s'.",
                    question_id,
                    attempt_id
                )

                raise QuestionNotFoundException()


            question_type = question.get(
                "question_type"
            )


            if (
                question_type
                == "multiple_select"
            ):

                if (
                    not isinstance(
                        answer,
                        list
                    )
                    or not answer
                    or len(
                        set(answer)
                    ) != len(answer)
                    or any(
                        selected_option
                        not in question["options"]
                        for selected_option in answer
                    )
                ):

                    logger.warning(
                        "Attempt submission failed: "
                        "invalid multiple-select answer "
                        "for question_id='%s'.",
                        question_id
                    )

                    raise InvalidAnswerException()


            elif (
                question_type
                == "short_answer"
            ):

                if (
                    not isinstance(
                        answer,
                        str
                    )
                    or not answer.strip()
                ):

                    logger.warning(
                        "Attempt submission failed: "
                        "invalid short answer "
                        "for question_id='%s'.",
                        question_id
                    )

                    raise InvalidAnswerException()


            else:

                if (
                    not isinstance(
                        answer,
                        str
                    )
                    or answer not in
                    question["options"]
                ):

                    logger.warning(
                        "Attempt submission failed: "
                        "invalid answer "
                        "for question_id='%s'.",
                        question_id
                    )

                    raise InvalidAnswerException()


        quiz = (
            QuizRepository.get_quiz_by_id(
                attempt["quiz_id"]
            )
        )


        if not quiz:

            logger.warning(
                "Attempt submission failed: "
                "quiz_id='%s' not found.",
                attempt["quiz_id"]
            )

            raise QuizNotFoundException()


        saved_answers = (
            attempt.get(
                "answers",
                {}
            )
        )


        final_answers = {
            **saved_answers,
            **request.answers
        }


        AttemptService._complete_attempt(
            attempt_id,
            attempt,
            final_answers,
            quiz
        )


        logger.info(
            "Attempt submitted successfully: "
            "attempt_id='%s', quiz_id='%s', "
            "student_id='%s'.",
            attempt_id,
            attempt["quiz_id"],
            current_user["sub"]
        )


        return AttemptMessageResponse(
            message=ErrorMessages.ATTEMPT_SUBMITTED
        )