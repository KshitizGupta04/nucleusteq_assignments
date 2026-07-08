from datetime import datetime

from app.constants.messages import (
    ErrorMessages
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
    UpdateCategoryRequest,
    CategoryCreateResponse,
    CategoryMessageResponse
)


class CategoryService:

    @staticmethod
    def create_category(
        request: CategoryRequest
    ):

        if CategoryRepository.get_category_by_name(
            request.name
        ):
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

        response = CategoryCreateResponse(
            message=ErrorMessages.CATEGORY_CREATED,
            category_id=category_id
        )

        return response

    @staticmethod
    def get_all_categories():

        response = (
            CategoryRepository.get_all_categories()
        )

        return response

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
            raise CategoryNotFoundException()

        category["_id"] = str(
            category["_id"]
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
            raise CategoryNotFoundException()

        existing_category = (
            CategoryRepository.get_category_by_name(
                request.name
            )
        )

        if (
            existing_category
            and str(existing_category["_id"]) != category_id
        ):
            raise CategoryAlreadyExistsException()

        CategoryRepository.update_category(
            category_id,
            {
                "name": request.name,
                "description": request.description,
                "updated_at": datetime.utcnow()
            }
        )

        response = CategoryMessageResponse(
            message=ErrorMessages.CATEGORY_UPDATED
        )

        return response

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
            raise CategoryNotFoundException()

        CategoryRepository.delete_category(
            category_id
        )

        response = CategoryMessageResponse(
            message=ErrorMessages.CATEGORY_DELETED
        )

        return response