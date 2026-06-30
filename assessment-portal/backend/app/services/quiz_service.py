from datetime import datetime

from app.constants.messages import (
    ErrorMessages
)

from app.exceptions.customexceptions import (
    CategoryNotFoundException,
    QuizAlreadyExistsException,
    QuizNotFoundException
)

from app.models.quiz import (
    Quiz
)

from app.repositories.category_repository import (
    CategoryRepository
)

from app.repositories.quiz_repository import (
    QuizRepository
)

from app.schemas.quiz_schema import (
    QuizRequest,
    UpdateQuizRequest
)


class QuizService:

    @staticmethod
    def create_quiz(
        request: QuizRequest
    ):

        if QuizRepository.get_quiz_by_title_and_category(
            request.title,
            request.category_id
        ):
            raise QuizAlreadyExistsException()

        category = (
            CategoryRepository.get_category_by_id(
                request.category_id
            )
        )

        if not category:
            raise CategoryNotFoundException()

        quiz = Quiz(
            title=request.title,
            description=request.description,
            category_id=request.category_id,
            duration=request.duration,
            total_marks=request.total_marks
        )

        quiz_id = (
            QuizRepository.create_quiz(
                quiz.model_dump()
            )
        )

        return {
            "message": ErrorMessages.QUIZ_CREATED,
            "quiz_id": quiz_id
        }

    @staticmethod
    def get_all_quizzes():

        return QuizRepository.get_all_quizzes()

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
            raise QuizNotFoundException()

        category = (
            CategoryRepository.get_category_by_id(
                request.category_id
            )
        )

        if not category:
            raise CategoryNotFoundException()

        QuizRepository.update_quiz(
            quiz_id,
            {
                "title": request.title,
                "description": request.description,
                "category_id": request.category_id,
                "duration": request.duration,
                "total_marks": request.total_marks,
                "updated_at": datetime.utcnow()
            }
        )

        return {
            "message": ErrorMessages.QUIZ_UPDATED
        }

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
            raise QuizNotFoundException()

        QuizRepository.delete_quiz(
            quiz_id
        )

        return {
            "message": ErrorMessages.QUIZ_DELETED
        }