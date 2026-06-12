from collections.abc import Generator

import pytest
from playwright.sync_api import Browser, Page, Playwright

from core.config import Settings, get_settings
from pages.dashboard_page import DashboardPage
from pages.statistics_page import StatisticsPage
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
    try:
        page = context.new_page()
        yield page
    finally:
        context.close()


@pytest.fixture()
def anonymous_page(browser: Browser) -> Generator[Page, None, None]:
    context = browser.new_context()
    try:
        page = context.new_page()
        yield page
    finally:
        context.close()


@pytest.fixture()
def dashboard_page(authenticated_page: Page, settings: Settings) -> DashboardPage:
    return DashboardPage(page=authenticated_page, base_url=settings.base_url)


@pytest.fixture()
def statistics_page(authenticated_page: Page, settings: Settings) -> StatisticsPage:
    return StatisticsPage(page=authenticated_page, base_url=settings.base_url)
