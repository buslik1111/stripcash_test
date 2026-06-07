from collections.abc import Generator

import pytest
from playwright.sync_api import Browser, Page, Playwright

from core.config import Settings, get_settings
from services.auth_service import AuthService


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest.fixture()
def authenticated_page(
    playwright: Playwright,
    browser: Browser,
    settings: Settings,
) -> Generator[Page, None, None]:
    storage_state = AuthService(
        playwright=playwright,
        api_base_url=settings.api_base_url,
    ).login(
        username=settings.login,
        password=settings.password,
    )

    context = browser.new_context(storage_state=storage_state)
    page = context.new_page()

    yield page

    context.close()
