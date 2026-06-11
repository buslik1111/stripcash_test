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
    statistics_timeout_seconds: int
    statistics_poll_interval_ms: int


def get_settings() -> Settings:
    load_dotenv()

    return Settings(
        login=_get_required_env("STRIPCASH_LOGIN"),
        password=_get_required_env("STRIPCASH_PASSWORD"),
        base_url=os.getenv("STRIPCASH_BASE_URL", "https://stripcash.com"),
        api_base_url=os.getenv("STRIPCASH_API_BASE_URL", "https://api.stripcash.com"),
        statistics_timeout_seconds=_get_int_env(
            name="STATISTICS_TIMEOUT_SECONDS",
            default=60,
        ),
        statistics_poll_interval_ms=_get_int_env(
            name="STATISTICS_POLL_INTERVAL_MS",
            default=5_000,
        ),
    )


def _get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(f"Environment variable {name} is required")

    return value


def _get_int_env(name: str, default: int) -> int:
    value = os.getenv(name)

    if value is None:
        return default

    try:
        return int(value)
    except ValueError as error:
        raise RuntimeError(f"Environment variable {name} must be integer") from error
