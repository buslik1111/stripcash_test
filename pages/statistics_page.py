import re
from time import monotonic
from urllib.parse import urlparse

from playwright.sync_api import Locator, Page, Response, TimeoutError, expect

from pages.base_page import BasePage


class StatisticsApiPaths:
    """Store API paths used to synchronize Statistics page actions."""

    REPORT = "/front/trafficStatistics"


class StatisticsButtons:
    """Store button names used on the Statistics page."""

    RUN_REPORT_BUTTON = "Run report"


class StatisticsTestIds:
    """Store data-testid values used on the Statistics page."""

    CHIP = "Chip"
    DROPDOWN_MENU_ITEM = "DropdownListDropdownMenuItem"
    TABLE = "Table"
    TABLE_HEAD = "TableHead"
    TABLE_CELL = "TableCell"
    TABS_TAB = "TabsTab"


class StatisticsTableText:
    """Store text markers used to read the statistics report."""

    CLICKS = "Clicks"
    FILTERS = "Filters"
    NO_DATA = "No suitable data"
    SOURCE = "Source"
    TOTAL = "Total"


class StatisticsSelectors:
    """Store CSS selectors used on the Statistics page."""

    REPORT_TABLE_CONTAINER = '[qa-element="summary-table"]'
    SOURCE_DROPDOWN = "#sourceId"
    SOURCE_SEARCH = "#sourceId-search"


class StatisticsPage(BasePage):
    """Provide actions and report data access for the Statistics page."""

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page=page, base_url=base_url)

    def open(self) -> None:
        self.open_path("/analytics/statistics")

    def run_report(self) -> None:
        run_report_button = self._page.get_by_role(
            "button",
            name=StatisticsButtons.RUN_REPORT_BUTTON,
            exact=True,
        )

        with self._page.expect_response(
            self._is_statistics_report_response,
            timeout=30_000,
        ) as response_info:
            run_report_button.click()

        response = response_info.value

        if not response.ok:
            raise RuntimeError(
                "Statistics report request failed: "
                f"status={response.status}, url={response.url}"
            )

        response.body()
        expect(self._report_table()).to_be_visible(timeout=30_000)

    def filter_by_source(
        self,
        source_id: str,
        timeout_seconds: int,
        interval_ms: int,
    ) -> None:
        """Select a source filter when the tracked source becomes available."""

        filters_tab = self._page.get_by_test_id(
            StatisticsTestIds.TABS_TAB
        ).filter(has_text=StatisticsTableText.FILTERS)
        expect(filters_tab).to_have_count(1)
        filters_tab.click()

        source_filter = self._page.get_by_test_id(
            StatisticsTestIds.CHIP
        ).filter(has_text=StatisticsTableText.SOURCE)
        expect(source_filter).to_have_count(1)
        source_filter.click()

        source_dropdown = self._page.locator(StatisticsSelectors.SOURCE_DROPDOWN)
        expect(source_dropdown).to_be_visible()
        source_dropdown.locator('[qa-element="spinner"]').wait_for(
            state="detached",
            timeout=30_000,
        )

        deadline = monotonic() + timeout_seconds
        source_option = self._page.get_by_test_id(
            StatisticsTestIds.DROPDOWN_MENU_ITEM
        ).filter(has_text=re.compile(rf"^{re.escape(source_id)}$"))
        source_search = self._page.locator(StatisticsSelectors.SOURCE_SEARCH)

        while monotonic() < deadline:
            if not source_search.is_visible():
                source_dropdown.click()

            source_search.fill(source_id)

            try:
                source_option.wait_for(state="visible", timeout=interval_ms)
            except TimeoutError:
                source_search.fill("")
                continue

            expect(source_option).to_have_count(1)
            source_option.click()
            return

        raise RuntimeError(f"Source was not found in statistics filters: {source_id}")

    def get_total_clicks(self) -> int:
        """Return the Total value from the Clicks column."""

        table = self._report_table()
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

    def wait_for_total_clicks(
        self,
        expected_clicks: int,
        timeout_seconds: int,
        interval_ms: int,
    ) -> int:
        """Rerun the report until the expected Clicks value is available."""

        deadline = monotonic() + timeout_seconds
        actual_clicks = 0

        while monotonic() < deadline:
            self.run_report()
            actual_clicks = self.get_total_clicks()

            if actual_clicks >= expected_clicks:
                return actual_clicks

            self._page.wait_for_timeout(interval_ms)

        return actual_clicks

    def _report_table(self) -> Locator:
        return self._page.locator(
            StatisticsSelectors.REPORT_TABLE_CONTAINER
        ).get_by_test_id(StatisticsTestIds.TABLE)

    @staticmethod
    def _is_statistics_report_response(response: Response) -> bool:
        return (
            response.request.method == "GET"
            and urlparse(response.url).path == StatisticsApiPaths.REPORT
        )
