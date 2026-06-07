from playwright.sync_api import Page, expect


class StatisticsPage:
    def __init__(self, page: Page, base_url: str) -> None:
        self._page = page
        self._base_url = base_url

    def open(self) -> None:
        self._page.goto(f"{self._base_url}/analytics/statistics")
        expect(self._page).to_have_url(f"{self._base_url}/analytics/statistics")

    def run_today_report(self) -> None:
        self._page.get_by_role("button", name="Today", exact=True).click()
        self._page.get_by_role("button", name="Run report", exact=True).click()

        table = self._page.get_by_test_id("Table")
        expect(table).to_be_visible()
        expect(table.get_by_text("CLICKS", exact=True)).to_be_visible()

    def get_total_clicks(self) -> int:
        table = self._page.get_by_test_id("Table")
        expect(table).to_be_visible()

        table_text = table.inner_text()
        rows = [row.strip() for row in table_text.splitlines() if row.strip()]

        try:
            total_index = rows.index("Total")
        except ValueError as error:
            raise RuntimeError(f"Total row was not found in report table: {rows}") from error

        if total_index == 0:
            raise RuntimeError(f"Clicks value was not found before Total row: {rows}")

        clicks = rows[total_index - 1]

        if not clicks.isdigit():
            raise RuntimeError(f"Unexpected clicks value: {clicks}")

        return int(clicks)
