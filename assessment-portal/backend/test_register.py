from app.models.user import UserRole

from app.schemas.auth_schema import (
    RegisterRequest
)

from app.services.auth_service import (
    AuthService
)


request = RegisterRequest(
    username="admin",
    email="admin@gmail.com",
    password="Admin@123"
)

result = AuthService.register_user(
    request,
    UserRole.ADMIN
)

print(result)