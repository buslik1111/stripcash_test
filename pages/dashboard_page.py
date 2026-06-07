from playwright.sync_api import Page, expect


class DashboardPage:
    def __init__(self, page: Page, base_url: str) -> None:
        self._page = page
        self._base_url = base_url

    def open(self) -> None:
        self._page.goto(f"{self._base_url}/overview/dashboard")
        expect(self._page).to_have_url(f"{self._base_url}/overview/dashboard")

    def get_default_link(self) -> str:
        default_link = self._page.get_by_test_id("LinkUrl")
        expect(default_link).to_be_visible()

        link = default_link.inner_text().strip()

        if not link.startswith("https://"):
            raise RuntimeError(f"Unexpected default link value: {link}")

        return link