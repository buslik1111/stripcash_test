from playwright.sync_api import Playwright, StorageState


class AuthService:
    """Authenticate through the API and return UI storage state."""

    def __init__(self, playwright: Playwright, api_base_url: str) -> None:
        self._playwright = playwright
        self._api_base_url = api_base_url

    def login(self, username: str, password: str) -> StorageState:
        """Log in through the API and prepare browser storage state."""

        request_context = self._playwright.request.new_context(
            base_url=self._api_base_url,
            extra_http_headers={
                "Origin": "https://stripcash.com",
                "Referer": "https://stripcash.com/login",
            },
        )

        try:
            response = request_context.post(
                "/front/v1/auth/login",
                data={
                    "usernameOrEmail": username,
                    "password": password,
                    "recaptchaToken": "",
                },
            )

            if not response.ok:
                raise RuntimeError(
                    f"Login failed with status {response.status}: {response.text()}"
                )

            return request_context.storage_state()
        finally:
            request_context.dispose()
