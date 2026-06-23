"""
User model helper functions.
"""

from datetime import datetime
from bson import ObjectId


def user_entity(user: dict) -> dict:
    """
    Convert a MongoDB user document into a JSON-serializable dictionary.
    """
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "created_at": user["created_at"],
    }


def user_collection(users) -> list:
    """
    Convert a list of MongoDB user documents.
    """
    return [user_entity(user) for user in users]


def create_user_document(
    name: str,
    email: str,
    password: str,
    role: str = "student",
) -> dict:
    """
    Create a MongoDB user document.
    """
    return {
        "name": name,
        "email": email,
        "password": password,
        "role": role,
        "created_at": datetime.utcnow(),
    }