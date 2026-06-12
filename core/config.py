import os
from dataclasses import dataclass
from urllib.parse import urlparse

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    """Store test settings loaded from environment variables."""

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
        base_url=_get_url_env(
            name="STRIPCASH_BASE_URL",
            default="https://stripcash.com",
        ),
        api_base_url=_get_url_env(
            name="STRIPCASH_API_BASE_URL",
            default="https://api.stripcash.com",
        ),
        statistics_timeout_seconds=_get_positive_int_env(
            name="STATISTICS_TIMEOUT_SECONDS",
            default=60,
        ),
        statistics_poll_interval_ms=_get_positive_int_env(
            name="STATISTICS_POLL_INTERVAL_MS",
            default=5_000,
        ),
    )


def _get_required_env(name: str) -> str:
    value = os.getenv(name)

    if value is None or not value.strip():
        raise RuntimeError(f"Environment variable {name} is required")

    return value


def _get_url_env(name: str, default: str) -> str:
    value = os.getenv(name, default).strip().rstrip("/")
    parsed_url = urlparse(value)

    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        raise RuntimeError(f"Environment variable {name} must be a valid HTTP URL")

    return value


def _get_positive_int_env(name: str, default: int) -> int:
    value = os.getenv(name)

    if value is None:
        return default

    try:
        parsed_value = int(value)
    except ValueError as error:
        raise RuntimeError(f"Environment variable {name} must be integer") from error

    if parsed_value <= 0:
        raise RuntimeError(f"Environment variable {name} must be greater than zero")

    return parsed_value
