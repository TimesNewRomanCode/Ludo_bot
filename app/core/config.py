from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, computed_field


class Settings(BaseSettings):
    DB_DRIVER: str = "asyncpg"
    DB_PROTOCOL: str = "postgresql"
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "Ludo"

    BOT_TOKEN: str = "1:1"

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"{self.DB_PROTOCOL}+{self.DB_DRIVER}://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @field_validator("BOT_TOKEN")
    @classmethod
    def validate_telegram_bot_token(cls, v: str) -> str:
        parts = v.split(":")
        if len(parts) != 2:
            raise ValueError("Token must be in format '<bot_id>:<bot_key>'")
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
