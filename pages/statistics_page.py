from time import monotonic

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class StatisticsButtons:
    """Хранит названия кнопок страницы Statistics"""

    RUN_REPORT_BUTTON = "Run report"


class StatisticsTestIds:
    """Хранит data-testid элементов страницы Statistics"""

    TABLE = "Table"
    TABLE_CELL = "TableCell"


class StatisticsTableText:
    """Хранит текстовые маркеры, которые используются при чтении отчета"""

    NO_DATA = "No suitable data"


class StatisticsPage(BasePage):
    """Описывает действия пользователя и чтение данных на странице Statistics"""

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
        """Возвращает Total по колонке Clicks из виртуальной таблицы отчета"""

        table = self._page.get_by_test_id(StatisticsTestIds.TABLE)
        expect(table).to_be_visible()

        if StatisticsTableText.NO_DATA in table.inner_text():
            return 0

        clicks_values = []
        cells = table.get_by_test_id(StatisticsTestIds.TABLE_CELL)

        for index in range(cells.count()):
            cell_text = cells.nth(index).inner_text().strip()

            if not cell_text:
                continue

            if not cell_text.isdigit():
                break

            clicks_values.append(int(cell_text))

        if not clicks_values:
            raise RuntimeError("Clicks values were not found in report table")

        return clicks_values[-1]

    def wait_for_total_clicks_increment(
        self,
        expected_clicks: int,
        timeout_seconds: int,
        interval_ms: int,
    ) -> int:
        """Перезапускает отчет, пока статистика не увидит новый клик"""

        deadline = monotonic() + timeout_seconds
        actual_clicks = expected_clicks - 1

        while monotonic() < deadline:
            self.open()
            self.run_report()
            actual_clicks = self.get_total_clicks()

            if actual_clicks >= expected_clicks:
                return actual_clicks

            self._page.wait_for_timeout(interval_ms)

        return actual_clicks
