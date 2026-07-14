from app.core.logger import (
    logger
)

from app.exceptions.customexceptions import (
    ForbiddenException,
    ResultAlreadyExistsException,
    ResultNotFoundException
)

from app.models.result import (
    Result
)

from app.repositories.attempt_repository import (
    AttemptRepository
)

from app.repositories.quiz_repository import (
    QuizRepository
)

from app.repositories.result_repository import (
    ResultRepository
)

from app.schemas.result_schema import (
    AdminResultResponse,
    LeaderboardResponse,
    QuestionBreakdownResponse,
    QuizStatisticsResponse,
    ResultHistoryResponse,
    ResultResponse
)


class ResultService:

    PASSING_PERCENTAGE = 40.0


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
    def _calculate_multiple_select_score(
        selected_answer: list,
        correct_answer: list,
        marks_per_question: float
    ) -> float:

        selected_answers = set(
            selected_answer
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
    def generate_result(
        attempt_id: str
    ):

        existing_result = (
            ResultRepository.get_result_by_attempt_id(
                attempt_id
            )
        )

        if existing_result:

            logger.warning(
                "Result generation failed: "
                "result already exists for "
                "attempt_id='%s'.",
                attempt_id
            )

            raise ResultAlreadyExistsException()


        attempt = (
            AttemptRepository.get_attempt_by_id(
                attempt_id
            )
        )

        if not attempt:

            logger.warning(
                "Result generation failed: "
                "attempt_id='%s' not found.",
                attempt_id
            )

            raise ResultNotFoundException()


        quiz = (
            QuizRepository.get_quiz_by_id(
                attempt["quiz_id"]
            )
        )

        if not quiz:

            logger.warning(
                "Result generation failed: "
                "quiz_id='%s' not found.",
                attempt["quiz_id"]
            )

            raise ResultNotFoundException()


        total_marks = float(
            quiz["total_marks"]
        )

        total_questions = len(
            attempt["question_snapshot"]
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


        question_breakdown = []

        score_obtained = 0.0


        for question in attempt[
            "question_snapshot"
        ]:

            question_id = (
                ResultService._get_question_id(
                    question
                )
            )

            selected_answer = (
                attempt.get(
                    "answers",
                    {}
                ).get(
                    question_id
                )
            )

            correct_answer = question[
                "correct_answer"
            ]

            question_type = question.get(
                "question_type",
                "mcq"
            )


            if selected_answer is None:

                is_correct = False

                marks_obtained = 0.0


            elif (
                question_type
                == "multiple_select"
            ):

                marks_obtained = (
                    ResultService
                    ._calculate_multiple_select_score(
                        selected_answer,
                        correct_answer,
                        marks_per_question
                    )
                )

                is_correct = (
                    set(selected_answer)
                    == set(correct_answer)
                )


            elif (
                question_type
                == "short_answer"
            ):

                is_correct = (
                    selected_answer
                    .strip()
                    .casefold()
                    ==
                    correct_answer
                    .strip()
                    .casefold()
                )

                if is_correct:

                    marks_obtained = (
                        marks_per_question
                    )

                else:

                    marks_obtained = (
                        -negative_marks
                    )


            else:

                is_correct = (
                    selected_answer
                    == correct_answer
                )

                if is_correct:

                    marks_obtained = (
                        marks_per_question
                    )

                else:

                    marks_obtained = (
                        -negative_marks
                    )


            score_obtained += (
                marks_obtained
            )


            question_breakdown.append(
                {
                    "question_id":
                        question_id,

                    "question":
                        question["question"],

                    "selected_answer":
                        selected_answer,

                    "correct_answer":
                        correct_answer,

                    "is_correct":
                        is_correct,

                    "marks_obtained":
                        marks_obtained
                }
            )


        score_obtained = max(
            score_obtained,
            0.0
        )


        percentage = (
            (
                score_obtained /
                total_marks
            ) * 100
            if total_marks > 0
            else 0.0
        )


        status = (
            "pass"
            if percentage >=
            ResultService.PASSING_PERCENTAGE
            else "fail"
        )


        result = Result(
            attempt_id=attempt_id,

            quiz_id=attempt[
                "quiz_id"
            ],

            student_id=attempt[
                "student_id"
            ],

            attempt_number=attempt[
                "attempt_number"
            ],

            score_obtained=score_obtained,

            total_marks=total_marks,

            percentage=percentage,

            status=status,

            question_breakdown=
                question_breakdown
        )


        result_id = (
            ResultRepository.create_result(
                result.model_dump()
            )
        )


        logger.info(
            "Result generated successfully: "
            "result_id='%s', attempt_id='%s', "
            "quiz_id='%s', student_id='%s', "
            "score='%s', percentage='%s', "
            "status='%s'.",
            result_id,
            attempt_id,
            attempt["quiz_id"],
            attempt["student_id"],
            score_obtained,
            percentage,
            status
        )


        return result_id


    @staticmethod
    def get_result_by_id(
        result_id: str,
        current_user
    ):

        result = (
            ResultRepository.get_result_by_id(
                result_id
            )
        )

        if not result:

            logger.warning(
                "Result retrieval failed: "
                "result_id='%s' not found.",
                result_id
            )

            raise ResultNotFoundException()


        if (
            current_user["role"] == "student"
            and result["student_id"] !=
            current_user["sub"]
        ):

            logger.warning(
                "Result access denied: "
                "student_id='%s' tried to access "
                "result_id='%s' owned by "
                "student_id='%s'.",
                current_user["sub"],
                result_id,
                result["student_id"]
            )

            raise ForbiddenException()


        return ResultResponse(
            result_id=str(
                result["_id"]
            ),

            attempt_id=result[
                "attempt_id"
            ],

            quiz_id=result[
                "quiz_id"
            ],

            student_id=result[
                "student_id"
            ],

            attempt_number=result[
                "attempt_number"
            ],

            score_obtained=result[
                "score_obtained"
            ],

            total_marks=result[
                "total_marks"
            ],

            percentage=result[
                "percentage"
            ],

            status=result[
                "status"
            ],

            question_breakdown=[
                QuestionBreakdownResponse(
                    **question
                )

                for question in result[
                    "question_breakdown"
                ]
            ]
        )


    @staticmethod
    def get_student_results(
        current_user
    ):

        results = (
            ResultRepository.get_results_by_student(
                current_user["sub"]
            )
        )


        return [
            ResultHistoryResponse(
                result_id=str(
                    result["_id"]
                ),

                attempt_id=result[
                    "attempt_id"
                ],

                quiz_id=result[
                    "quiz_id"
                ],

                attempt_number=result[
                    "attempt_number"
                ],

                score_obtained=result[
                    "score_obtained"
                ],

                total_marks=result[
                    "total_marks"
                ],

                percentage=result[
                    "percentage"
                ],

                status=result[
                    "status"
                ]
            )

            for result in results
        ]


    @staticmethod
    def get_result_breakdown(
        result_id: str,
        current_user
    ):

        result = (
            ResultRepository.get_result_by_id(
                result_id
            )
        )

        if not result:

            logger.warning(
                "Result breakdown retrieval failed: "
                "result_id='%s' not found.",
                result_id
            )

            raise ResultNotFoundException()


        if (
            current_user["role"] == "student"
            and result["student_id"] !=
            current_user["sub"]
        ):

            logger.warning(
                "Result breakdown access denied: "
                "student_id='%s' tried to access "
                "result_id='%s' owned by "
                "student_id='%s'.",
                current_user["sub"],
                result_id,
                result["student_id"]
            )

            raise ForbiddenException()


        return [
            QuestionBreakdownResponse(
                **question
            )

            for question in result[
                "question_breakdown"
            ]
        ]


    @staticmethod
    def get_admin_dashboard():

        results = (
            ResultRepository.get_all_results()
        )


        return [
            AdminResultResponse(
                result_id=str(
                    result["_id"]
                ),

                attempt_id=result[
                    "attempt_id"
                ],

                quiz_id=result[
                    "quiz_id"
                ],

                student_id=result[
                    "student_id"
                ],

                attempt_number=result[
                    "attempt_number"
                ],

                score_obtained=result[
                    "score_obtained"
                ],

                total_marks=result[
                    "total_marks"
                ],

                percentage=result[
                    "percentage"
                ],

                status=result[
                    "status"
                ]
            )

            for result in results
        ]


    @staticmethod
    def get_quiz_statistics(
        quiz_id: str
    ):

        quiz = (
            QuizRepository.get_quiz_by_id(
                quiz_id
            )
        )

        if not quiz:

            logger.warning(
                "Quiz statistics retrieval failed: "
                "quiz_id='%s' not found.",
                quiz_id
            )

            raise ResultNotFoundException()


        results = (
            ResultRepository.get_results_by_quiz(
                quiz_id
            )
        )


        total_attempts = len(
            results
        )


        if total_attempts == 0:

            return QuizStatisticsResponse(
                quiz_id=quiz_id,
                total_attempts=0,
                average_score=0.0,
                pass_count=0,
                fail_count=0,
                pass_rate=0.0
            )


        total_percentage = sum(
            float(
                result["percentage"]
            )
            for result in results
        )


        pass_count = sum(
            1
            for result in results
            if result["status"] == "pass"
        )


        fail_count = (
            total_attempts
            - pass_count
        )


        average_score = round(
            total_percentage /
            total_attempts,
            2
        )


        pass_rate = round(
            (
                pass_count /
                total_attempts
            ) * 100,
            2
        )


        return QuizStatisticsResponse(
            quiz_id=quiz_id,
            total_attempts=total_attempts,
            average_score=average_score,
            pass_count=pass_count,
            fail_count=fail_count,
            pass_rate=pass_rate
        )


    @staticmethod
    def get_quiz_leaderboard(
        quiz_id: str
    ):

        quiz = (
            QuizRepository.get_quiz_by_id(
                quiz_id
            )
        )

        if not quiz:

            logger.warning(
                "Quiz leaderboard retrieval failed: "
                "quiz_id='%s' not found.",
                quiz_id
            )

            raise ResultNotFoundException()


        results = (
            ResultRepository.get_results_by_quiz(
                quiz_id
            )
        )


        best_results = {}


        for result in results:

            student_id = result[
                "student_id"
            ]


            if student_id not in best_results:

                best_results[
                    student_id
                ] = result

                continue


            existing_result = (
                best_results[
                    student_id
                ]
            )


            if (
                float(
                    result["percentage"]
                )
                >
                float(
                    existing_result[
                        "percentage"
                    ]
                )
            ):

                best_results[
                    student_id
                ] = result


        sorted_results = sorted(
            best_results.values(),

            key=lambda result: (
                float(
                    result["percentage"]
                ),

                float(
                    result["score_obtained"]
                )
            ),

            reverse=True
        )


        return [
            LeaderboardResponse(
                rank=index,

                student_id=result[
                    "student_id"
                ],

                score_obtained=result[
                    "score_obtained"
                ],

                total_marks=result[
                    "total_marks"
                ],

                percentage=result[
                    "percentage"
                ]
            )

            for index, result in enumerate(
                sorted_results,
                start=1
            )
        ]