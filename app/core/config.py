from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    SECRET_KEY: str

    ALGORITHM: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int

    TELEGRAM_BOT_TOKEN: str = ""

    ADMIN_EMAIL: str = ""
    ADMIN_PASSWORD: str = ""

    class Config:
        env_file = ".env"


settings = Settings()