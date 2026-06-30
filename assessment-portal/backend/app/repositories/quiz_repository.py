from bson import ObjectId

from app.core.database import db


class QuizRepository:

    collection = db["quizzes"]

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
    def get_quiz_by_title(
        cls,
        title: str
    ):

        return cls.collection.find_one(
            {
                "title": title
            }
        )

    @classmethod
    def get_quiz_by_id(
        cls,
        quiz_id: str
    ):

        return cls.collection.find_one(
            {
                "_id": ObjectId(
                    quiz_id
                )
            }
        )

    @classmethod
    def get_all_quizzes(
        cls
    ):

        quizzes = list(
            cls.collection.find()
        )

        for quiz in quizzes:

            quiz["_id"] = str(
                quiz["_id"]
            )

        return quizzes

    @classmethod
    def update_quiz(
        cls,
        quiz_id: str,
        quiz_data: dict
    ):

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

    @classmethod
    def delete_quiz(
        cls,
        quiz_id: str
    ):

        return cls.collection.delete_one(
            {
                "_id": ObjectId(
                    quiz_id
                )
            }
        )