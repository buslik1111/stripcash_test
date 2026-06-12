from playwright.sync_api import Page

from core.config import Settings
from pages.dashboard_page import DashboardPage
from pages.statistics_page import StatisticsPage
from utils.tracking import build_unique_tracking_link
from validations.assert_wrappers import assert_greater


def test_default_link_click_is_reflected_in_statistics(
    authenticated_page: Page,
    anonymous_page: Page,
    dashboard_page: DashboardPage,
    statistics_page: StatisticsPage,
    settings: Settings,
) -> None:
    dashboard_page.open()
    tracking_link = build_unique_tracking_link(dashboard_page.get_default_link())

    statistics_page.open()
    statistics_page.run_report()
    clicks_before = statistics_page.get_total_clicks()

    anonymous_page.goto(tracking_link, wait_until="domcontentloaded")

    clicks_after = statistics_page.wait_for_total_clicks_increment(
        clicks_before=clicks_before,
        timeout_seconds=settings.statistics_timeout_seconds,
        interval_ms=settings.statistics_poll_interval_ms,
    )

    assert_greater(
        actual_value=clicks_after,
        expected_value=clicks_before,
        error_msg=(
            "Click count was not increased after opening default link: "
            f"before={clicks_before}, after={clicks_after}"
        ),
    )
