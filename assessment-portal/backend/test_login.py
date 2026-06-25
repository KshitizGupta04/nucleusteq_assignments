from app.services.auth_service import (
    AuthService
)


result = AuthService.login_user(
    "admin",
    "Admin@123"
)

print(result)