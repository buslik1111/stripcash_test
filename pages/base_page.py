from playwright.sync_api import Page, expect


class BasePage:
    """Provide common URL navigation for page objects."""

    def __init__(self, page: Page, base_url: str) -> None:
        self._page = page
        self._base_url = base_url

    def open_path(self, path: str) -> None:
        url = f"{self._base_url}{path}"
        self._page.goto(url, wait_until="domcontentloaded")
        expect(self._page).to_have_url(url)
