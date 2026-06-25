from bson import ObjectId

from app.core.database import db


class UserRepository:

    collection = db["users"]

    @classmethod
    def create_user(
        cls,
        user_data: dict
    ):
        result = cls.collection.insert_one(
            user_data
        )

        return str(
            result.inserted_id
        )

    @classmethod
    def get_user_by_email(
        cls,
        email: str
    ):
        return cls.collection.find_one(
            {"email": email}
        )

    @classmethod
    def get_user_by_username(
        cls,
        username: str
    ):
        return cls.collection.find_one(
            {"username": username}
        )

    @classmethod
    def admin_exists(cls):
        return cls.collection.find_one(
            {"role": "admin"}
        )

    @classmethod
    def get_user_by_id(
        cls,
        user_id: str
    ):
        return cls.collection.find_one(
            {
                "_id": ObjectId(user_id)
            }
        )

    @classmethod
    def get_all_users(cls):
        users = list(
            cls.collection.find(
                {},
                {
                    "password": 0
                }
            )
        )

        for user in users:
            user["_id"] = str(user["_id"])

        return users