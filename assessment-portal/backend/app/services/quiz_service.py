from datetime import datetime

from app.constants.messages import (
    ErrorMessages
)

from app.core.logger import (
    logger
)

from app.exceptions.customexceptions import (
    CategoryNotFoundException,
    QuizAlreadyExistsException,
    QuizNotFoundException
)

from app.models.quiz import (
    Quiz
)

from app.repositories.attempt_repository import (
    AttemptRepository
)

from app.repositories.category_repository import (
    CategoryRepository
)

from app.repositories.question_repository import (
    QuestionRepository
)

from app.repositories.quiz_repository import (
    QuizRepository
)

from app.repositories.result_repository import (
    ResultRepository
)

from app.schemas.quiz_schema import (
    QuizRequest,
    UpdateQuizRequest,
    QuizCreateResponse,
    QuizMessageResponse
)


class QuizService:

    MAX_ATTEMPTS = 3


    @staticmethod
    def create_quiz(
        request: QuizRequest
    ):

        if QuizRepository.get_quiz_by_title_and_category(
            request.title,
            request.category_id
        ):

            logger.warning(
                "Quiz creation failed: "
                "quiz title '%s' already exists "
                "in category_id='%s'.",
                request.title,
                request.category_id
            )

            raise QuizAlreadyExistsException()


        category = (
            CategoryRepository.get_category_by_id(
                request.category_id
            )
        )


        if not category:

            logger.warning(
                "Quiz creation failed: "
                "category_id='%s' not found.",
                request.category_id
            )

            raise CategoryNotFoundException()


        quiz = Quiz(
            title=request.title,
            description=request.description,
            category_id=request.category_id,
            duration=request.duration,
            total_marks=request.total_marks,
            question_count=request.question_count,
            negative_marks=request.negative_marks,
            available_from=request.available_from,
            available_until=request.available_until
        )


        quiz_id = (
            QuizRepository.create_quiz(
                quiz.model_dump()
            )
        )


        logger.info(
            "Quiz created successfully: "
            "quiz_id='%s', title='%s', "
            "category_id='%s'.",
            quiz_id,
            request.title,
            request.category_id
        )


        response = QuizCreateResponse(
            message=ErrorMessages.QUIZ_CREATED,
            quiz_id=quiz_id
        )

        return response


    @staticmethod
    def get_all_quizzes(
        current_user
    ):

        quizzes = (
            QuizRepository.get_all_quizzes()
        )


        if (
            current_user.get("role")
            != "student"
        ):

            return quizzes


        student_id = current_user["sub"]

        response = []


        for quiz in quizzes:

            quiz_data = quiz.copy()

            quiz_id = str(
                quiz_data.get(
                    "id",
                    quiz_data.get(
                        "_id",
                        ""
                    )
                )
            )


            attempt_count = (
                AttemptRepository.count_attempts(
                    student_id,
                    quiz_id
                )
            )


            remaining_attempts = max(
                QuizService.MAX_ATTEMPTS
                - attempt_count,
                0
            )


            quiz_data[
                "max_attempts"
            ] = QuizService.MAX_ATTEMPTS

            quiz_data[
                "attempts_used"
            ] = attempt_count

            quiz_data[
                "remaining_attempts"
            ] = remaining_attempts


            response.append(
                quiz_data
            )


        return response


    @staticmethod
    def update_quiz(
        quiz_id: str,
        request: UpdateQuizRequest
    ):

        quiz = (
            QuizRepository.get_quiz_by_id(
                quiz_id
            )
        )


        if not quiz:

            logger.warning(
                "Quiz update failed: "
                "quiz_id='%s' not found.",
                quiz_id
            )

            raise QuizNotFoundException()


        category = (
            CategoryRepository.get_category_by_id(
                request.category_id
            )
        )


        if not category:

            logger.warning(
                "Quiz update failed: "
                "category_id='%s' not found "
                "for quiz_id='%s'.",
                request.category_id,
                quiz_id
            )

            raise CategoryNotFoundException()


        QuizRepository.update_quiz(
            quiz_id,
            {
                "title": request.title,
                "description": request.description,
                "category_id": request.category_id,
                "duration": request.duration,
                "total_marks": request.total_marks,
                "question_count": request.question_count,
                "negative_marks": request.negative_marks,
                "available_from": request.available_from,
                "available_until": request.available_until,
                "updated_at": datetime.utcnow()
            }
        )


        logger.info(
            "Quiz updated successfully: "
            "quiz_id='%s', title='%s', "
            "category_id='%s'.",
            quiz_id,
            request.title,
            request.category_id
        )


        response = QuizMessageResponse(
            message=ErrorMessages.QUIZ_UPDATED
        )

        return response


    @staticmethod
    def delete_quiz(
        quiz_id: str
    ):

        quiz = (
            QuizRepository.get_quiz_by_id(
                quiz_id
            )
        )


        if not quiz:

            logger.warning(
                "Quiz deletion failed: "
                "quiz_id='%s' not found.",
                quiz_id
            )

            raise QuizNotFoundException()


        # Delete dependent data first to prevent
        # orphaned records in the database.
        questions_result = (
            QuestionRepository
            .delete_questions_by_quiz(
                quiz_id
            )
        )


        attempts_result = (
            AttemptRepository
            .delete_attempts_by_quiz(
                quiz_id
            )
        )


        results_result = (
            ResultRepository
            .delete_results_by_quiz(
                quiz_id
            )
        )


        # Delete the parent quiz only after its
        # dependent records have been removed.
        QuizRepository.delete_quiz(
            quiz_id
        )


        logger.info(
            "Quiz deleted with cascade: "
            "quiz_id='%s', questions_deleted=%s, "
            "attempts_deleted=%s, "
            "results_deleted=%s.",
            quiz_id,
            questions_result.deleted_count,
            attempts_result.deleted_count,
            results_result.deleted_count
        )


        response = QuizMessageResponse(
            message=ErrorMessages.QUIZ_DELETED
        )

        return response