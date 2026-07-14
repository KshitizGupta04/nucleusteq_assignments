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


    @staticmethod
    def _serialize_category(
        category: dict | None
    ):

        if not category:

            return None

        category = category.copy()

        category["id"] = str(
            category.pop("_id")
        )

        return category


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

        except (
            InvalidId,
            TypeError
        ):

            return None


    @classmethod
    def get_all_categories(
        cls,
        page: int | None = None,
        limit: int | None = None
    ):

        query = cls.collection.find()

        # Apply pagination only when both page
        # and limit are explicitly provided.
        if (
            page is not None
            and limit is not None
        ):

            skip = (
                page - 1
            ) * limit

            query = (
                query
                .skip(skip)
                .limit(limit)
            )

        categories = list(
            query
        )

        return [
            cls._serialize_category(
                category
            )
            for category in categories
        ]


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

        except (
            InvalidId,
            TypeError
        ):

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

        except (
            InvalidId,
            TypeError
        ):

            return None