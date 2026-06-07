from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class StatisticsButtons:
    """Хранит названия кнопок страницы Statistics."""

    RUN_REPORT_BUTTON = "Run report"


class StatisticsTestIds:
    """Хранит data-testid элементов страницы Statistics."""

    TABLE = "Table"


class StatisticsTableText:
    """Хранит текстовые маркеры, которые используются при чтении отчета."""

    NO_DATA = "No suitable data"
    CLICKS_HEADER = "CLICKS"
    GROUP_HEADER = "GROUP"


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

        table_text = table.inner_text()
        if StatisticsTableText.NO_DATA in table_text:
            return 0

        rows = [row.strip() for row in table_text.splitlines() if row.strip()]

        try:
            clicks_index = rows.index(StatisticsTableText.CLICKS_HEADER)
            group_index = rows.index(StatisticsTableText.GROUP_HEADER)
        except ValueError as error:
            raise RuntimeError(f"Report table has unexpected structure: {rows}") from error

        clicks_values = [
            int(row)
            for row in rows[clicks_index + 1 : group_index]
            if row.isdigit()
        ]

        if not clicks_values:
            raise RuntimeError(f"Clicks values were not found in report table: {rows}")

        return clicks_values[-1]
