from app.repositories.user_repository import UserRepository


user_id = UserRepository.create_user(
    {
        "username": "admin",
        "email": "admin@gmail.com",
        "password": "test123"
    }
)

print("USER ID:")
print(user_id)

print()

user = UserRepository.get_user_by_email(
    "admin@gmail.com"
)

print(user)