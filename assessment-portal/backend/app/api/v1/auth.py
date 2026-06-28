from fastapi import (
    APIRouter,
    Depends
)

from fastapi.security import (
    OAuth2PasswordRequestForm
)

from app.core.dependencies import (
    get_current_admin,
    get_current_user
)

from app.enums.user_role import (
    UserRole
)

from app.repositories.user_repository import (
    UserRepository
)

from app.schemas.auth_schema import (
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
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

    return AuthService.register_user(
        request,
        UserRole.STUDENT
    )


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    request: LoginRequest
):

    return AuthService.login_user(
        request.username,
        request.password
    )


@router.post(
    "/token",
    response_model=TokenResponse
)
def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    return AuthService.login_user(
        form_data.username,
        form_data.password
    )


@router.post(
    "/refresh",
    response_model=TokenResponse
)
def refresh_token(
    request: RefreshTokenRequest
):

    return AuthService.refresh_access_token(
        request.refresh_token
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