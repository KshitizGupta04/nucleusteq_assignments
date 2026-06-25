from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.models.user import (
    User,
    UserRole
)

from app.repositories.user_repository import (
    UserRepository
)

from app.schemas.auth_schema import (
    RegisterRequest
)


class AuthService:

    @staticmethod
    def register_user(
        request: RegisterRequest,
        role: UserRole = UserRole.STUDENT
    ):

        existing_email = (
            UserRepository.get_user_by_email(
                request.email
            )
        )

        if existing_email:
            raise ValueError(
                "Email already registered"
            )

        existing_username = (
            UserRepository.get_user_by_username(
                request.username
            )
        )

        if existing_username:
            raise ValueError(
                "Username already exists"
            )

        if role == UserRole.ADMIN:

            existing_admin = (
                UserRepository.admin_exists()
            )

            if existing_admin:
                raise ValueError(
                    "Admin already exists"
                )

        user = User(
            username=request.username,
            email=request.email,
            password=hash_password(
                request.password
            ),
            role=role
        )

        user_id = UserRepository.create_user(
            user.model_dump()
        )

        return {
            "message":
            "User registered successfully",
            "user_id": user_id
        }

    @staticmethod
    def login_user(
        username: str,
        password: str
    ):

        user = (
            UserRepository.get_user_by_username(
                username
            )
        )

        if not user:
            raise ValueError(
                "User not found"
            )

        if not verify_password(
            password,
            user["password"]
        ):
            raise ValueError(
                "Invalid password"
            )

        access_token = (
            create_access_token(
                {
                    "sub":
                    user["username"],

                    "role":
                    user["role"]
                }
            )
        )

        return {
            "access_token":
            access_token,

            "token_type":
            "bearer"
        }