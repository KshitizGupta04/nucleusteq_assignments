from fastapi import (
    APIRouter,
    Depends
)

from app.core.dependencies import (
    get_current_admin,
    get_current_user
)

from app.schemas.category_schema import (
    CategoryRequest,
    UpdateCategoryRequest
)

from app.services.category_service import (
    CategoryService
)


router = APIRouter(
    prefix="/api/v1/categories",
    tags=["Category"]
)


@router.post("/")
def create_category(
    request: CategoryRequest,
    current_admin=Depends(
        get_current_admin
    )
):

    return CategoryService.create_category(
        request
    )


@router.get("/")
def get_categories(
    current_user=Depends(
        get_current_user
    )
):

    return CategoryService.get_all_categories()


@router.get("/{category_id}")
def get_category(
    category_id: str,
    current_user=Depends(
        get_current_user
    )
):

    return CategoryService.get_category_by_id(
        category_id
    )


@router.put("/{category_id}")
def update_category(
    category_id: str,
    request: UpdateCategoryRequest,
    current_admin=Depends(
        get_current_admin
    )
):

    return CategoryService.update_category(
        category_id,
        request
    )


@router.delete("/{category_id}")
def delete_category(
    category_id: str,
    current_admin=Depends(
        get_current_admin
    )
):

    return CategoryService.delete_category(
        category_id
    )