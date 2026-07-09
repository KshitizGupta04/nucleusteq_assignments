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
    QuestionBreakdownResponse,
    ResultHistoryResponse,
    ResultResponse
)


class ResultService:

    PASSING_PERCENTAGE = 40.0

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

            raise ResultAlreadyExistsException()

        attempt = (
            AttemptRepository.get_attempt_by_id(
                attempt_id
            )
        )

        if not attempt:

            raise ResultNotFoundException()

        quiz = (
            QuizRepository.get_quiz_by_id(
                attempt["quiz_id"]
            )
        )

        if not quiz:

            raise ResultNotFoundException()

        total_marks = float(
            quiz["total_marks"]
        )

        total_questions = len(
            attempt["question_snapshot"]
        )

        if total_questions > 0:

            marks_per_question = (
                total_marks /
                total_questions
            )

        else:

            marks_per_question = 0.0

        question_breakdown = []

        score_obtained = 0.0

        for question in attempt[
            "question_snapshot"
        ]:

            question_id = str(
                question["_id"]
            )

            selected_answer = (
                attempt["answers"].get(
                    question_id
                )
            )

            correct_answer = question[
                "correct_answer"
            ]

            is_correct = (
                selected_answer is not None
                and selected_answer
                == correct_answer
            )

            marks_obtained = (
                marks_per_question
                if is_correct
                else 0.0
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

        if total_marks > 0:

            percentage = (
                score_obtained /
                total_marks
            ) * 100

        else:

            percentage = 0.0

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
            question_breakdown=question_breakdown
        )

        result_id = (
            ResultRepository.create_result(
                result.model_dump()
            )
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

            raise ResultNotFoundException()

        if (
            current_user["role"] == "student"
            and result["student_id"]
            != current_user["sub"]
        ):

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

            raise ResultNotFoundException()

        if (
            current_user["role"] == "student"
            and result["student_id"]
            != current_user["sub"]
        ):

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