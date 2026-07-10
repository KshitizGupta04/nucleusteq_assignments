from datetime import (
    datetime
)

from bson import (
    ObjectId
)

from bson.errors import (
    InvalidId
)

from app.core.database import (
    db
)


class AttemptRepository:

    collection = db["attempts"]

    @classmethod
    def create_attempt(
        cls,
        attempt_data: dict
    ):

        result = cls.collection.insert_one(
            attempt_data
        )

        return str(
            result.inserted_id
        )

    @classmethod
    def get_attempt_by_id(
        cls,
        attempt_id: str
    ):

        try:

            return cls.collection.find_one(
                {
                    "_id": ObjectId(
                        attempt_id
                    )
                }
            )

        except InvalidId:

            return None

    @classmethod
    def get_attempts_by_student_and_quiz(
        cls,
        student_id: str,
        quiz_id: str
    ):

        return list(
            cls.collection.find(
                {
                    "student_id": student_id,
                    "quiz_id": quiz_id
                }
            )
        )

    @classmethod
    def get_attempts_by_student(
        cls,
        student_id: str
    ):

        attempts = list(
            cls.collection.find(
                {
                    "student_id": student_id
                }
            )
        )

        for attempt in attempts:

            attempt["_id"] = str(
                attempt["_id"]
            )

        return attempts

    @classmethod
    def get_attempts_by_quiz(
        cls,
        quiz_id: str
    ):

        attempts = list(
            cls.collection.find(
                {
                    "quiz_id": quiz_id
                }
            )
        )

        for attempt in attempts:

            attempt["_id"] = str(
                attempt["_id"]
            )

        return attempts

    @classmethod
    def count_attempts(
        cls,
        student_id: str,
        quiz_id: str
    ):

        return cls.collection.count_documents(
            {
                "student_id": student_id,
                "quiz_id": quiz_id
            }
        )

    @classmethod
    def get_in_progress_attempt(
        cls,
        student_id: str,
        quiz_id: str
    ):

        return cls.collection.find_one(
            {
                "student_id": student_id,
                "quiz_id": quiz_id,
                "status": "in_progress"
            }
        )

    @classmethod
    def save_answer(
        cls,
        attempt_id: str,
        question_id: str,
        answer: str
    ):

        try:

            return cls.collection.update_one(
                {
                    "_id": ObjectId(
                        attempt_id
                    )
                },
                {
                    "$set": {
                        f"answers.{question_id}": answer,
                        "updated_at": datetime.utcnow()
                    }
                }
            )

        except InvalidId:

            return None

    @classmethod
    def submit_attempt(
        cls,
        attempt_id: str,
        score: int
    ):

        try:

            return cls.collection.update_one(
                {
                    "_id": ObjectId(
                        attempt_id
                    )
                },
                {
                    "$set": {
                        "score": score,
                        "status": "submitted",
                        "submitted_at": datetime.utcnow(),
                        "updated_at": datetime.utcnow()
                    }
                }
            )

        except InvalidId:

            return None

    @classmethod
    def update_attempt(
        cls,
        attempt_id: str,
        attempt_data: dict
    ):

        try:

            attempt_data[
                "updated_at"
            ] = datetime.utcnow()

            return cls.collection.update_one(
                {
                    "_id": ObjectId(
                        attempt_id
                    )
                },
                {
                    "$set": attempt_data
                }
            )

        except InvalidId:

            return None

    @classmethod
    def delete_attempt(
        cls,
        attempt_id: str
    ):

        try:

            return cls.collection.delete_one(
                {
                    "_id": ObjectId(
                        attempt_id
                    )
                }
            )

        except InvalidId:

            return None