from time import monotonic

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class StatisticsButtons:
    """Store button names used on the Statistics page."""

    RUN_REPORT_BUTTON = "Run report"


class StatisticsTestIds:
    """Store data-testid values used on the Statistics page."""

    TABLE = "Table"
    TABLE_HEAD = "TableHead"
    TABLE_CELL = "TableCell"


class StatisticsTableText:
    """Store text markers used to read the statistics report."""

    CLICKS = "Clicks"
    NO_DATA = "No suitable data"
    TOTAL = "Total"


class StatisticsPage(BasePage):
    """Provide actions and report data access for the Statistics page."""

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page=page, base_url=base_url)

    def open(self) -> None:
        self.open_path("/analytics/statistics")

    def run_report(self) -> None:
        self._page.get_by_role(
            "button",
            name=StatisticsButtons.RUN_REPORT_BUTTON,
            exact=True,
        ).click()

        table = self._page.get_by_test_id(StatisticsTestIds.TABLE)
        expect(table).to_be_visible(timeout=30_000)

    def get_total_clicks(self) -> int:
        """Return the Total value from the Clicks column."""

        table = self._page.get_by_test_id(StatisticsTestIds.TABLE)
        expect(table).to_be_visible()

        if StatisticsTableText.NO_DATA in table.inner_text():
            return 0

        clicks_header = table.get_by_test_id(StatisticsTestIds.TABLE_HEAD).filter(
            has_text=StatisticsTableText.CLICKS
        )
        total_cell = table.get_by_test_id(StatisticsTestIds.TABLE_CELL).filter(
            has_text=StatisticsTableText.TOTAL
        )
        expect(clicks_header).to_have_count(1)
        expect(total_cell).to_have_count(1)

        column_index = clicks_header.get_attribute("data-column-index")
        row_index = total_cell.get_attribute("data-row-index")

        if column_index is None or row_index is None:
            raise RuntimeError("Statistics table indexes were not found")

        clicks_total_cell = table.locator(
            f'[data-testid="{StatisticsTestIds.TABLE_CELL}"]'
            f'[data-column-index="{column_index}"]'
            f'[data-row-index="{row_index}"]'
        )
        expect(clicks_total_cell).to_have_count(1)

        clicks_value = (
            clicks_total_cell.inner_text().strip().replace(",", "").replace(" ", "")
        )

        if not clicks_value.isdigit():
            raise RuntimeError(f"Unexpected Clicks total value: {clicks_value}")

        return int(clicks_value)

    def wait_for_total_clicks_increment(
        self,
        clicks_before: int,
        timeout_seconds: int,
        interval_ms: int,
    ) -> int:
        """Rerun the report until the total Clicks value increases."""

        deadline = monotonic() + timeout_seconds
        actual_clicks = clicks_before

        while monotonic() < deadline:
            self.run_report()
            actual_clicks = self.get_total_clicks()

            if actual_clicks > clicks_before:
                return actual_clicks

            self._page.wait_for_timeout(interval_ms)

        return actual_clicks
