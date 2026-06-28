from app.core.security import create_access_token
from app.core.dependencies import get_current_user


token = create_access_token(
    {
        "sub": "admin@gmail.com",
        "role": "admin"
    }
)

payload = get_current_user(token)

print(payload)