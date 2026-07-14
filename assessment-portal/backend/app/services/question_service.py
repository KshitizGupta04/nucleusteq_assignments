from datetime import datetime

from app.constants.messages import (
    ErrorMessages
)

from app.core.logger import (
    logger
)

from app.exceptions.customexceptions import (
    QuestionNotFoundException,
    QuizNotFoundException
)

from app.models.question import (
    Question
)

from app.repositories.question_repository import (
    QuestionRepository
)

from app.repositories.quiz_repository import (
    QuizRepository
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

            logger.warning(
                "Question creation failed: "
                "quiz_id='%s' not found.",
                request.quiz_id
            )

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

        logger.info(
            "Question created successfully: "
            "question_id='%s', quiz_id='%s', "
            "question_type='%s'.",
            question_id,
            request.quiz_id,
            request.question_type
        )

        return {
            "message": ErrorMessages.QUESTION_CREATED,
            "question_id": question_id
        }


    @staticmethod
    def get_questions_by_quiz(
        quiz_id: str,
        include_correct_answer: bool = False
    ):

        quiz = (
            QuizRepository.get_quiz_by_id(
                quiz_id
            )
        )

        if not quiz:

            logger.warning(
                "Question retrieval failed: "
                "quiz_id='%s' not found.",
                quiz_id
            )

            raise QuizNotFoundException()

        questions = (
            QuestionRepository.get_questions_by_quiz_id(
                quiz_id
            )
        )

        if include_correct_answer:

            return questions

        return [
            {
                key: value
                for key, value in question.items()
                if key != "correct_answer"
            }
            for question in questions
        ]


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

            logger.warning(
                "Question update failed: "
                "question_id='%s' not found.",
                question_id
            )

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

        logger.info(
            "Question updated successfully: "
            "question_id='%s', "
            "question_type='%s'.",
            question_id,
            request.question_type
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

            logger.warning(
                "Question deletion failed: "
                "question_id='%s' not found.",
                question_id
            )

            raise QuestionNotFoundException()

        QuestionRepository.delete_question(
            question_id
        )

        logger.info(
            "Question deleted successfully: "
            "question_id='%s'.",
            question_id
        )

        return {
            "message": ErrorMessages.QUESTION_DELETED
        }