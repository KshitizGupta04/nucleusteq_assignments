from bson import (
    ObjectId
)

from bson.errors import (
    InvalidId
)

from app.core.database import (
    db
)


class QuestionRepository:

    collection = db["questions"]


    @staticmethod
    def _serialize_question(
        question
    ):

        if not question:

            return None

        question = question.copy()

        question["id"] = str(
            question.pop("_id")
        )

        return question


    @classmethod
    def create_question(
        cls,
        question_data: dict
    ):

        result = cls.collection.insert_one(
            question_data
        )

        return str(
            result.inserted_id
        )


    @classmethod
    def get_question_by_id(
        cls,
        question_id: str
    ):

        try:

            return cls.collection.find_one(
                {
                    "_id": ObjectId(
                        question_id
                    )
                }
            )

        except (
            InvalidId,
            TypeError
        ):

            return None


    @classmethod
    def get_questions_by_quiz_id(
        cls,
        quiz_id: str
    ):

        questions = list(
            cls.collection.find(
                {
                    "quiz_id": quiz_id
                }
            )
        )

        return [
            cls._serialize_question(
                question
            )
            for question in questions
        ]


    @classmethod
    def update_question(
        cls,
        question_id: str,
        question_data: dict
    ):

        try:

            return cls.collection.update_one(
                {
                    "_id": ObjectId(
                        question_id
                    )
                },
                {
                    "$set": question_data
                }
            )

        except (
            InvalidId,
            TypeError
        ):

            return None


    @classmethod
    def delete_question(
        cls,
        question_id: str
    ):

        try:

            return cls.collection.delete_one(
                {
                    "_id": ObjectId(
                        question_id
                    )
                }
            )

        except (
            InvalidId,
            TypeError
        ):

            return None