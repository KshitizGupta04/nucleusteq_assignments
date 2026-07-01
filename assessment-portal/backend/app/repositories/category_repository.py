from bson import (
    ObjectId
)

from bson.errors import (
    InvalidId
)

from app.core.database import (
    db
)


class CategoryRepository:

    collection = db["categories"]

    @classmethod
    def create_category(
        cls,
        category_data: dict
    ):

        result = cls.collection.insert_one(
            category_data
        )

        return str(
            result.inserted_id
        )

    @classmethod
    def get_category_by_name(
        cls,
        name: str
    ):

        return cls.collection.find_one(
            {
                "name": name
            }
        )

    @classmethod
    def get_category_by_id(
        cls,
        category_id: str
    ):

        try:

            return cls.collection.find_one(
                {
                    "_id": ObjectId(
                        category_id
                    )
                }
            )

        except InvalidId:

            return None

    @classmethod
    def get_all_categories(
        cls
    ):

        categories = list(
            cls.collection.find()
        )

        for category in categories:

            category["_id"] = str(
                category["_id"]
            )

        return categories

    @classmethod
    def update_category(
        cls,
        category_id: str,
        category_data: dict
    ):

        try:

            return cls.collection.update_one(
                {
                    "_id": ObjectId(
                        category_id
                    )
                },
                {
                    "$set": category_data
                }
            )

        except InvalidId:

            return None

    @classmethod
    def delete_category(
        cls,
        category_id: str
    ):

        try:

            return cls.collection.delete_one(
                {
                    "_id": ObjectId(
                        category_id
                    )
                }
            )

        except InvalidId:

            return None