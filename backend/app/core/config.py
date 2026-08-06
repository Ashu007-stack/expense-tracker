from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Expense Tracker API"
    APP_VERSION: str = "1.0.0"

    DATABASE_URL: str = "sqlite:///./expense_tracker.db"

    SECRET_KEY: str = "change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore",
        )
    
settings = Settings()