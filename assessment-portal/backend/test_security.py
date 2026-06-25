from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)


password = "Admin@123"

hashed = hash_password(password)

print("HASHED PASSWORD:")
print(hashed)

print()

print(
    "PASSWORD VERIFIED:",
    verify_password(
        password,
        hashed
    )
)

print()

token = create_access_token(
    {
        "sub": "kshitiz@gmail.com",
        "role": "admin"
    }
)

print("JWT TOKEN:")
print(token)

print()

decoded = decode_access_token(token)

print("DECODED TOKEN:")
print(decoded)