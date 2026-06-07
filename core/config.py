import os

from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    """Хранит настройки запуска тестов, загруженные из переменных окружения."""

    login: str
    password: str
    base_url: str
    api_base_url: str


def get_settings() -> Settings:
    load_dotenv()

    return Settings(
        login=_get_required_env("STRIPCASH_LOGIN"),
        password=_get_required_env("STRIPCASH_PASSWORD"),
        base_url=os.getenv("STRIPCASH_BASE_URL", "https://stripcash.com"),
        api_base_url=os.getenv("STRIPCASH_API_BASE_URL", "https://api.stripcash.com"),
    )


def _get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(f"Environment variable {name} is required")

    return value
