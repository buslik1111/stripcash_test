from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class StatisticsButtons:
    """Хранит названия кнопок страницы Statistics."""

    RUN_REPORT_BUTTON = "Run report"


class StatisticsTestIds:
    """Хранит data-testid элементов страницы Statistics."""

    TABLE = "Table"
    TABLE_CELL = "TableCell"


class StatisticsTableText:
    """Хранит текстовые маркеры, которые используются при чтении отчета."""

    NO_DATA = "No suitable data"


class StatisticsPage(BasePage):
    """Описывает действия пользователя и чтение данных на странице Statistics."""

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
        """Возвращает Total по колонке Clicks из виртуальной таблицы отчета."""

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
