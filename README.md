# Stripcash default link test

## Overview

This project contains an automated test for the following scenario:

1. Authenticate at `https://stripcash.com` through the API.
2. Open `/overview/dashboard`.
3. Get the current `Default link`.
4. Open the tracking link in a separate anonymous browser context.
5. Open `/analytics/statistics`.
6. Filter the report by the generated source.
7. Click `Run report` and verify that the report contains exactly one click.

The login and password are not stored in the source code. The test reads them
from environment variables.

## Technology stack

- Python
- Pytest
- Playwright
- pytest-playwright
- python-dotenv
- Ruff

## Project structure

```text
core/          project configuration
pages/         Page Object classes
services/      test state preparation services
tests/         test scenarios
utils/         utility functions
validations/   assertion helpers
```

## Environment setup

Create a `.env` file based on `.env.example`:

```text
STRIPCASH_LOGIN=your_login_here
STRIPCASH_PASSWORD=your_password_here
STRIPCASH_BASE_URL=https://stripcash.com
STRIPCASH_API_BASE_URL=https://api.stripcash.com
STATISTICS_TIMEOUT_SECONDS=60
STATISTICS_POLL_INTERVAL_MS=5000
```

## Local execution

Install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m playwright install chromium
```

Run the test:

```bash
python3 -m pytest
```

Run the test in headed mode:

```bash
python3 -m pytest --headed --slowmo 500
```

Run the linter:

```bash
python3 -m ruff check .
```

## Docker

Build the image:

```bash
docker build -t stripcash-tests .
```

Run the test:

```bash
docker run --rm --env-file .env stripcash-tests
```

## Implementation details

- Authentication is performed through the API to avoid depending on reCAPTCHA
  on the UI login page.
- A unique `sourceId` is added to the `Default link` and used as a report
  filter. This isolates the click created by each test during parallel runs.
- Statistics are updated asynchronously, so the test reruns the report until
  the new click appears or the timeout expires.
