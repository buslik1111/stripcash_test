from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class DashboardTestIds:
    """Хранит data-testid элементов страницы Dashboard"""

    DEFAULT_LINK = "LinkUrl"


class DashboardPage(BasePage):
    """Описывает действия пользователя на странице Dashboard"""

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page=page, base_url=base_url)

    def open(self) -> None:
        self.open_path("/overview/dashboard")

    def get_default_link(self) -> str:
        default_link = self._page.get_by_test_id(DashboardTestIds.DEFAULT_LINK)
        expect(default_link).to_be_visible()

        link = default_link.inner_text().strip()

        if not link.startswith("https://"):
            raise RuntimeError(f"Unexpected default link value: {link}")

        return link
