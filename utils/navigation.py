from playwright.sync_api import Error, Page


def open_tracking_link(page: Page, tracking_link: str) -> None:
    """Открывает tracking link и игнорирует допустимый обрыв соединения на редиректе."""

    try:
        page.goto(tracking_link, wait_until="domcontentloaded")
    except Error as error:
        if "ERR_CONNECTION_CLOSED" not in str(error):
            raise
