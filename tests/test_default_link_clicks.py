from playwright.sync_api import Page

from core.config import Settings
from pages.dashboard_page import DashboardPage
from pages.statistics_page import StatisticsPage
from utils.tracking import build_unique_tracking_link
from validations.assert_wrappers import assert_equal


def test_default_link_click_is_reflected_in_statistics(
    authenticated_page: Page,
    anonymous_page: Page,
    dashboard_page: DashboardPage,
    statistics_page: StatisticsPage,
    settings: Settings,
) -> None:
    dashboard_page.open()
    tracking_link, source_id = build_unique_tracking_link(
        dashboard_page.get_default_link()
    )

    anonymous_page.goto(tracking_link, wait_until="domcontentloaded")

    statistics_page.open()
    statistics_page.filter_by_source(
        source_id=source_id,
        timeout_seconds=settings.statistics_timeout_seconds,
        interval_ms=settings.statistics_poll_interval_ms,
    )
    total_clicks = statistics_page.wait_for_total_clicks(
        expected_clicks=1,
        timeout_seconds=settings.statistics_timeout_seconds,
        interval_ms=settings.statistics_poll_interval_ms,
    )

    assert_equal(
        actual_value=total_clicks,
        expected_value=1,
        error_msg=(
            "Unexpected click count for the test source: "
            f"source_id={source_id}, clicks={total_clicks}"
        ),
    )
