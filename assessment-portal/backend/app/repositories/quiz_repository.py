from bson import (
    ObjectId
)

from bson.errors import (
    InvalidId
)

from app.core.database import (
    db
)


class QuizRepository:

    collection = db["quizzes"]


    @staticmethod
    def _serialize_quiz(
        quiz: dict | None
    ):

        if not quiz:

            return None

        quiz = quiz.copy()

        quiz["id"] = str(
            quiz.pop("_id")
        )

        return quiz


    @classmethod
    def create_quiz(
        cls,
        quiz_data: dict
    ):

        result = cls.collection.insert_one(
            quiz_data
        )

        return str(
            result.inserted_id
        )


    @classmethod
    def get_quiz_by_title_and_category(
        cls,
        title: str,
        category_id: str
    ):

        return cls.collection.find_one(
            {
                "title": title,
                "category_id": category_id
            }
        )


    @classmethod
    def get_quiz_by_id(
        cls,
        quiz_id: str
    ):

        try:

            return cls.collection.find_one(
                {
                    "_id": ObjectId(
                        quiz_id
                    )
                }
            )

        except (
            InvalidId,
            TypeError
        ):

            return None


    @classmethod
    def get_all_quizzes(
        cls
    ):

        quizzes = list(
            cls.collection.find()
        )

        return [
            cls._serialize_quiz(
                quiz
            )
            for quiz in quizzes
        ]


    @classmethod
    def update_quiz(
        cls,
        quiz_id: str,
        quiz_data: dict
    ):

        try:

            return cls.collection.update_one(
                {
                    "_id": ObjectId(
                        quiz_id
                    )
                },
                {
                    "$set": quiz_data
                }
            )

        except (
            InvalidId,
            TypeError
        ):

            return None


    @classmethod
    def delete_quiz(
        cls,
        quiz_id: str
    ):

        try:

            return cls.collection.delete_one(
                {
                    "_id": ObjectId(
                        quiz_id
                    )
                }
            )

        except (
            InvalidId,
            TypeError
        ):

            return None