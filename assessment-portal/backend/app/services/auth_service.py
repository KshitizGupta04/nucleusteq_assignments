from app.constants.messages import ErrorMessages
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    hash_password,
    verify_password,
)
from app.enums.user_role import UserRole
from app.exceptions.customexceptions import (
    AdminAlreadyExistsException,
    InvalidPasswordException,
    InvalidTokenException,
    UserAlreadyExistsException,
    UserNotFoundException,
    UsernameAlreadyExistsException,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import RegisterRequest


class AuthService:

    @staticmethod
    def register_user(
        request: RegisterRequest,
        role: UserRole = UserRole.STUDENT,
    ) -> dict:

        if UserRepository.get_user_by_email(request.email):
            raise UserAlreadyExistsException()

        if UserRepository.get_user_by_username(request.username):
            raise UsernameAlreadyExistsException()

        if (
            role == UserRole.ADMIN
            and UserRepository.admin_exists()
        ):
            raise AdminAlreadyExistsException()

        user = User(
            username=request.username,
            email=request.email,
            password=hash_password(request.password),
            role=role,
        )

        user_id = UserRepository.create_user(
            user.model_dump()
        )

        return {
            "message": ErrorMessages.REGISTER_SUCCESS,
            "user_id": user_id,
        }

    @staticmethod
    def login_user(
        username: str,
        password: str,
    ) -> dict:

        user = UserRepository.get_user_by_username(
            username
        )

        if not user:
            raise UserNotFoundException()

        if not verify_password(
            password,
            user["password"],
        ):
            raise InvalidPasswordException()

        payload = {
            "sub": user["username"],
            "role": user["role"],
        }

        access_token = create_access_token(payload)

        refresh_token = create_refresh_token(payload)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    @staticmethod
    def refresh_access_token(
        refresh_token: str,
    ) -> dict:

        payload = decode_refresh_token(
            refresh_token
        )

        if not payload:
            raise InvalidTokenException()

        access_token = create_access_token(
            {
                "sub": payload["sub"],
                "role": payload["role"],
            }
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }