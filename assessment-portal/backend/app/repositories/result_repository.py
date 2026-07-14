from bson import (
    ObjectId
)

from bson.errors import (
    InvalidId
)

from app.core.database import (
    db
)


class ResultRepository:

    collection = db["results"]


    @classmethod
    def create_result(
        cls,
        result_data: dict
    ):

        result = cls.collection.insert_one(
            result_data
        )

        return str(
            result.inserted_id
        )


    @classmethod
    def get_result_by_id(
        cls,
        result_id: str
    ):

        try:

            return cls.collection.find_one(
                {
                    "_id": ObjectId(
                        result_id
                    )
                }
            )

        except InvalidId:

            return None


    @classmethod
    def get_result_by_attempt_id(
        cls,
        attempt_id: str
    ):

        return cls.collection.find_one(
            {
                "attempt_id": attempt_id
            }
        )


    @classmethod
    def get_results_by_student(
        cls,
        student_id: str
    ):

        results = list(
            cls.collection.find(
                {
                    "student_id": student_id
                }
            ).sort(
                "created_at",
                -1
            )
        )

        for result in results:

            result["_id"] = str(
                result["_id"]
            )

        return results


    @classmethod
    def get_results_by_quiz(
        cls,
        quiz_id: str
    ):

        results = list(
            cls.collection.find(
                {
                    "quiz_id": quiz_id
                }
            ).sort(
                "created_at",
                -1
            )
        )

        for result in results:

            result["_id"] = str(
                result["_id"]
            )

        return results


    @classmethod
    def get_all_results(
        cls
    ):

        results = list(
            cls.collection.find().sort(
                "created_at",
                -1
            )
        )

        for result in results:

            result["_id"] = str(
                result["_id"]
            )

        return results


    # Delete all results belonging to a quiz.
    @classmethod
    def delete_results_by_quiz(
        cls,
        quiz_id: str
    ):

        return cls.collection.delete_many(
            {
                "quiz_id": quiz_id
            }
        )