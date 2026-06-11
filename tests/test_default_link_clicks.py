from playwright.sync_api import Page

from core.config import Settings
from pages.dashboard_page import DashboardPage
from pages.statistics_page import StatisticsPage
from utils.tracking import build_unique_tracking_link
from validations.assert_wrappers import assert_greater_or_equal


def test_default_link_click_is_reflected_in_statistics(
    authenticated_page: Page,
    anonymous_page: Page,
    dashboard_page: DashboardPage,
    statistics_page: StatisticsPage,
    settings: Settings,
) -> None:
    statistics_page.open()
    statistics_page.run_report()
    clicks_before = statistics_page.get_total_clicks()

    dashboard_page.open()
    tracking_link = build_unique_tracking_link(dashboard_page.get_default_link())
    anonymous_page.goto(tracking_link, wait_until="domcontentloaded")

    clicks_after = statistics_page.wait_for_total_clicks_increment(
        expected_clicks=clicks_before + 1,
        timeout_seconds=settings.statistics_timeout_seconds,
        interval_ms=settings.statistics_poll_interval_ms,
    )

    assert_greater_or_equal(
        actual_value=clicks_after,
        expected_value=clicks_before + 1,
        error_msg=(
            "Click count was not increased after opening default link: "
            f"before={clicks_before}, after={clicks_after}"
        ),
    )
