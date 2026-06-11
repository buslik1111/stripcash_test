# Stripcash default link test

## Описание

Проект содержит автотест для проверки сценария из тестового задания:

1. Авторизоваться в `https://stripcash.com` через API.
2. Открыть `/overview/dashboard`.
3. Получить текущий `Default link`.
4. Перейти по tracking-ссылке в отдельной анонимной браузерной сессии.
5. Открыть `/analytics/statistics`.
6. Нажать `Run report`.
7. Проверить, что значение в колонке `Clicks` увеличилось минимум на 1.

Логин и пароль не хранятся в коде. Тест читает их из переменных окружения.

## Стек

- Python
- Pytest
- Playwright
- pytest-playwright
- python-dotenv
- Ruff

## Структура

```text
core/          настройки проекта
pages/         Page Object классы
services/      сервисы для подготовки тестового состояния
tests/         тестовые сценарии
utils/         вспомогательные функции
validations/   assertion helpers
```

## Настройка окружения

Создайте файл `.env` по примеру `.env.example`:

```text
STRIPCASH_LOGIN=your_login_here
STRIPCASH_PASSWORD=your_password_here
STRIPCASH_BASE_URL=https://stripcash.com
STRIPCASH_API_BASE_URL=https://api.stripcash.com
STATISTICS_TIMEOUT_SECONDS=60
STATISTICS_POLL_INTERVAL_MS=5000
```

## Локальный запуск

Установите зависимости:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m playwright install chromium
```

Запустите тест:

```bash
python3 -m pytest
```

Запуск в видимом браузере:

```bash
python3 -m pytest --headed --slowmo 500
```

Проверка стиля:

```bash
python3 -m ruff check .
```

## Docker

Соберите image:

```bash
docker build -t stripcash-tests .
```

Запустите тесты:

```bash
docker run --rm --env-file .env stripcash-tests
```

## Особенности теста

- Авторизация выполняется через API, чтобы не зависеть от reCAPTCHA на UI login.
- Перед переходом к `Default link` в ссылку добавляется уникальный `sourceId`, чтобы tracking-система не склеила повторные клики.
- Статистика обновляется не мгновенно, поэтому тест повторно запускает отчет до появления нового клика или до истечения таймаута.
