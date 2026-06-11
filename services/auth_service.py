from playwright.sync_api import Playwright, StorageState


class AuthService:
    """Авторизует пользователя через API и возвращает storage state для UI-теста"""

    def __init__(self, playwright: Playwright, api_base_url: str) -> None:
        self._playwright = playwright
        self._api_base_url = api_base_url

    def login(self, username: str, password: str) -> StorageState:
        """Выполняет API-логин и подготавливает storage state для браузерной сессии"""

        request_context = self._playwright.request.new_context(
            base_url=self._api_base_url,
            extra_http_headers={
                "Origin": "https://stripcash.com",
                "Referer": "https://stripcash.com/login",
            },
        )

        response = request_context.post(
            "/front/v1/auth/login",
            data={
                "usernameOrEmail": username,
                "password": password,
                "recaptchaToken": "",
            },
        )

        if not response.ok:
            request_context.dispose()
            raise RuntimeError(
                f"Login failed with status {response.status}: {response.text()}"
            )

        storage_state = request_context.storage_state()
        request_context.dispose()

        return storage_state
