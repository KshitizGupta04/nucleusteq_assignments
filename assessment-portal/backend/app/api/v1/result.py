from fastapi import (
    APIRouter,
    Depends
)

from app.core.dependencies import (
    get_current_admin,
    get_current_user,
    get_current_student
)

from app.services.result_service import (
    ResultService
)


router = APIRouter(
    prefix="/api/v1/results",
    tags=["Result"]
)


@router.get("/me")
def get_my_results(
    current_user=Depends(
        get_current_student
    )
):

    return ResultService.get_student_results(
        current_user
    )


@router.get("/admin/dashboard")
def get_admin_dashboard(
    current_admin=Depends(
        get_current_admin
    )
):

    return ResultService.get_admin_dashboard()


@router.get(
    "/admin/quiz/{quiz_id}/statistics"
)
def get_quiz_statistics(
    quiz_id: str,
    current_admin=Depends(
        get_current_admin
    )
):

    return ResultService.get_quiz_statistics(
        quiz_id
    )


@router.get(
    "/admin/quiz/{quiz_id}/leaderboard"
)
def get_quiz_leaderboard(
    quiz_id: str,
    current_admin=Depends(
        get_current_admin
    )
):

    return ResultService.get_quiz_leaderboard(
        quiz_id
    )

@router.get("/{result_id}/breakdown")
def get_result_breakdown(
    result_id: str,
    current_user=Depends(
        get_current_user
    )
):

    return ResultService.get_result_breakdown(
        result_id,
        current_user
    )


@router.get("/{result_id}")
def get_result_by_id(
    result_id: str,
    current_user=Depends(
        get_current_user
    )
):

    return ResultService.get_result_by_id(
        result_id,
        current_user
    )