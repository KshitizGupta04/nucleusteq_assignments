from datetime import datetime

from app.constants.messages import (
    ErrorMessages
)

from app.core.logger import (
    logger
)

from app.exceptions.customexceptions import (
    CategoryAlreadyExistsException,
    CategoryNotFoundException
)

from app.models.category import (
    Category
)

from app.repositories.category_repository import (
    CategoryRepository
)

from app.schemas.category_schema import (
    CategoryRequest,
    UpdateCategoryRequest
)


class CategoryService:

    @staticmethod
    def create_category(
        request: CategoryRequest
    ):

        existing_category = (
            CategoryRepository.get_category_by_name(
                request.name
            )
        )

        if existing_category:

            logger.warning(
                "Category creation failed: "
                "category name '%s' already exists.",
                request.name
            )

            raise CategoryAlreadyExistsException()

        category = Category(
            name=request.name,
            description=request.description
        )

        category_id = (
            CategoryRepository.create_category(
                category.model_dump()
            )
        )

        logger.info(
            "Category created successfully: "
            "category_id='%s', name='%s'.",
            category_id,
            request.name
        )

        return {
            "message": ErrorMessages.CATEGORY_CREATED,
            "category_id": category_id
        }


    @staticmethod
    def get_all_categories(
        page: int | None = None,
        limit: int | None = None
    ):

        return (
            CategoryRepository.get_all_categories(
                page=page,
                limit=limit
            )
        )


    @staticmethod
    def get_category_by_id(
        category_id: str
    ):

        category = (
            CategoryRepository.get_category_by_id(
                category_id
            )
        )

        if not category:

            logger.warning(
                "Category retrieval failed: "
                "category_id='%s' not found.",
                category_id
            )

            raise CategoryNotFoundException()

        category = category.copy()

        category["id"] = str(
            category.pop("_id")
        )

        return category


    @staticmethod
    def update_category(
        category_id: str,
        request: UpdateCategoryRequest
    ):

        category = (
            CategoryRepository.get_category_by_id(
                category_id
            )
        )

        if not category:

            logger.warning(
                "Category update failed: "
                "category_id='%s' not found.",
                category_id
            )

            raise CategoryNotFoundException()

        existing_category = (
            CategoryRepository.get_category_by_name(
                request.name
            )
        )

        if (
            existing_category
            and str(
                existing_category["_id"]
            ) != category_id
        ):

            logger.warning(
                "Category update failed: "
                "category name '%s' already exists.",
                request.name
            )

            raise CategoryAlreadyExistsException()

        CategoryRepository.update_category(
            category_id,
            {
                "name": request.name,
                "description": request.description,
                "updated_at": datetime.utcnow()
            }
        )

        logger.info(
            "Category updated successfully: "
            "category_id='%s', name='%s'.",
            category_id,
            request.name
        )

        return {
            "message": ErrorMessages.CATEGORY_UPDATED
        }


    @staticmethod
    def delete_category(
        category_id: str
    ):

        category = (
            CategoryRepository.get_category_by_id(
                category_id
            )
        )

        if not category:

            logger.warning(
                "Category deletion failed: "
                "category_id='%s' not found.",
                category_id
            )

            raise CategoryNotFoundException()

        CategoryRepository.delete_category(
            category_id
        )

        logger.info(
            "Category deleted successfully: "
            "category_id='%s'.",
            category_id
        )

        return {
            "message": ErrorMessages.CATEGORY_DELETED
        }