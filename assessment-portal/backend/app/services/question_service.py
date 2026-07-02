from datetime import datetime

from app.constants.messages import (
    ErrorMessages
)

from app.exceptions.customexceptions import (
    QuizNotFoundException,
    QuestionNotFoundException
)

from app.models.question import (
    Question
)

from app.repositories.quiz_repository import (
    QuizRepository
)

from app.repositories.question_repository import (
    QuestionRepository
)

from app.schemas.question_schema import (
    QuestionRequest,
    UpdateQuestionRequest
)


class QuestionService:

    @staticmethod
    def create_question(
        request: QuestionRequest
    ):

        quiz = (
            QuizRepository.get_quiz_by_id(
                request.quiz_id
            )
        )

        if not quiz:

            raise QuizNotFoundException()

        question = Question(
            quiz_id=request.quiz_id,
            question=request.question,
            options=request.options,
            correct_answer=request.correct_answer,
            question_type=request.question_type,
            difficulty=request.difficulty
        )

        question_id = (
            QuestionRepository.create_question(
                question.model_dump()
            )
        )

        return {
            "message": ErrorMessages.QUESTION_CREATED,
            "question_id": question_id
        }

    @staticmethod
    def get_questions_by_quiz(
        quiz_id: str
    ):

        quiz = (
            QuizRepository.get_quiz_by_id(
                quiz_id
            )
        )

        if not quiz:

            raise QuizNotFoundException()

        return (
            QuestionRepository.get_questions_by_quiz_id(
                quiz_id
            )
        )

    @staticmethod
    def update_question(
        question_id: str,
        request: UpdateQuestionRequest
    ):

        question = (
            QuestionRepository.get_question_by_id(
                question_id
            )
        )

        if not question:

            raise QuestionNotFoundException()

        QuestionRepository.update_question(
            question_id,
            {
                "question": request.question,
                "options": request.options,
                "correct_answer": request.correct_answer,
                "question_type": request.question_type,
                "difficulty": request.difficulty,
                "updated_at": datetime.utcnow()
            }
        )

        return {
            "message": ErrorMessages.QUESTION_UPDATED
        }

    @staticmethod
    def delete_question(
        question_id: str
    ):

        question = (
            QuestionRepository.get_question_by_id(
                question_id
            )
        )

        if not question:

            raise QuestionNotFoundException()

        QuestionRepository.delete_question(
            question_id
        )

        return {
            "message": ErrorMessages.QUESTION_DELETED
        }