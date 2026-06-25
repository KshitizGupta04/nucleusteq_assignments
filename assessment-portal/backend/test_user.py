from app.models.user import User

user = User(
    username="kshitiz",
    email="kshitiz@gmail.com",
    password="123456"
)

print(user.model_dump())