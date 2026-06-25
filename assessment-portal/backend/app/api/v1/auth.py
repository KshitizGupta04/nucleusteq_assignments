from fastapi.security import OAuth2PasswordRequestForm




from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from fastapi.security import (
    OAuth2PasswordRequestForm
)

from app.core.dependencies import (
    get_current_admin,
    get_current_user
)

from app.models.user import UserRole


from app.repositories.user_repository import (
    UserRepository
)

from app.schemas.auth_schema import (
    RegisterRequest,
    LoginRequest
)

from app.services.auth_service import (
    AuthService
)


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register_student(
    request: RegisterRequest
):

    try:

        return AuthService.register_user(
            request,
            UserRole.STUDENT
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/login")
def login(
    request: LoginRequest
):

    try:

        return AuthService.login_user(
            request.username,
            request.password
        )

    except ValueError as e:

        raise HTTPException(
            status_code=401,
            detail=str(e)
        )


@router.post("/token")
def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    try:

        return AuthService.login_user(
            form_data.username,
            form_data.password
        )

    except ValueError as e:

        raise HTTPException(
            status_code=401,
            detail=str(e)
        )


@router.get("/me")
def get_profile(
    current_user=Depends(
        get_current_user
    )
):

    return current_user


@router.get("/users")
def get_users(
    current_admin=Depends(
        get_current_admin
    )
):

    return UserRepository.get_all_users()