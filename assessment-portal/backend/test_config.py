from app.core.config import Settings

try:
    settings = Settings()
    print(settings.model_dump())
except Exception as e:
    print(type(e))
    print(e)