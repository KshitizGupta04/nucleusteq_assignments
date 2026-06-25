from app.core.database import db

db["users"].delete_many({})

print("All users deleted")